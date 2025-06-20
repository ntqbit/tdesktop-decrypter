import sys
import json
import argparse

from typing import Dict, Any, Optional

from .decrypter import (
    ParsedTdata,
    TdataReader,
    ParsedAccount,
    SettingsBlock,
    NoKeyFileException,
)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def display_accounts(accounts: Dict[int, ParsedAccount]):
    for account in accounts.values():
        print(f"Account {account.index}:")

        print("MTP data:")
        print(f"User ID: {account.mtp_data.user_id}")
        print(f"Main DC ID: {account.mtp_data.current_dc_id}")

        for dc_id, key in account.mtp_data.keys.items():
            print(f"Key DC {dc_id}: {key.hex()}")


def display_setting_value(setting: Any) -> str:
    if isinstance(setting, bytes):
        return setting.hex()

    if isinstance(setting, dict):
        return {k: display_setting_value(v) for k, v in setting.items()}

    if isinstance(setting, list):
        return [display_setting_value(v) for v in setting]

    assert any(isinstance(setting, c) for c in (int, float, str))
    return setting


def display_settings(settings: Optional[Dict[SettingsBlock, Any]]):
    if settings is None:
        print("No settings found.")
        return

    for setting_block, value in settings.items():
        print(f"{setting_block}: {display_setting_value(value)}")


def display_stdout(parsed_tdata: ParsedTdata, show_settings: bool):
    display_accounts(parsed_tdata.accounts)

    if show_settings:
        display_settings(parsed_tdata.settings)


def display_json(parsed_tdata: ParsedTdata):
    accounts = [
        {
            "index": account.index,
            "user_id": account.mtp_data.user_id,
            "main_dc_id": account.mtp_data.current_dc_id,
            "dc_auth_keys": {
                dc_id: key.hex().lower() for dc_id, key in account.mtp_data.keys.items()
            },
        }
        for account in parsed_tdata.accounts.values()
    ]

    if parsed_tdata.settings is None:
        settings = None
    else:
        settings = {
            str(k): display_setting_value(v) for k, v in parsed_tdata.settings.items()
        }

    obj = {
        "accounts": accounts,
        "settings": settings,
    }

    # Settings
    print(json.dumps(obj, indent=4))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tdata", type=str, help="Path to tdata/ directory")
    parser.add_argument(
        "--passcode", "-p", type=str, default=None, required=False, help="Passcode"
    )
    parser.add_argument(
        "--show_settings",
        action="store_true",
        help="Show decrypted settings",
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()

    reader = TdataReader(args.tdata)

    try:
        parsed_tdata = reader.read(args.passcode)

        if args.json:
            display_json(parsed_tdata)
        else:
            display_stdout(parsed_tdata, args.show_settings)
    except NoKeyFileException as exc:
        eprint("No key file was found. Is the tdata path correct?")
