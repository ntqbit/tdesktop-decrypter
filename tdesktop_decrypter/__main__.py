from typing import Dict, Any, Optional

from .decrypter import TdataReader, ParsedAccount, SettingsBlock


def display_accounts(accounts: Dict[int, ParsedAccount]):
    for account in accounts.values():
        print(f'Account {account.index}:')

        print('MTP data:')
        print(f'User ID: {account.mtp_data.user_id}')
        print(f'Main DC ID: {account.mtp_data.current_dc_id}')

        for dc_id, key in account.mtp_data.keys.items():
            print(f'Key DC {dc_id}: {key.hex(" ")}')


def display_settings(settings: Optional[Dict[SettingsBlock, Any]]):
    if settings is None:
        print('No settings found.')
        return

    for setting_block, value in settings.items():
        print(f'{setting_block}: {value}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tdata', type=str, help='Path to tdata/ directory')
    parser.add_argument('passcode', type=str, default=None, required=False, help='Passcode')
    parser.add_argument('show_settings', type=bool, action='store_true', help='Show decrypted settings')
    args = parser.parse_args()

    reader = TdataReader(args.tdata)
    
    parsed_tdata = reader.read(args.passcode)
    
    display_accounts(parsed_tdata.accounts)
    
    if args.show_settings:
        display_settings(parsed_tdata.settings)
    