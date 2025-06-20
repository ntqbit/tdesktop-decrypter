# Telegram Desktop tdata decrypter
Inspired by [telegram-desktop-decrypt](https://github.com/atilaromero/telegram-desktop-decrypt)

## Features
- Accounts MTP auth data decryption (User ID, DC ID, DC keys)
- Settings decryption

## Installation
Install with pipx (recommended):
```bash
pipx install git+https://github.com/ntqbit/tdesktop-decrypter.git
```

Install with pip:
```bash
pip install git+https://github.com/ntqbit/tdesktop-decrypter.git
```

## Usage
Run as executable:
```bash
tdesktop-decrypter arguments
```
Or run as python module:
```bash
python -m tdesktop_decrypter arguments
```

### Arguments
- `tdata` - path to tdata folder containing `settings` (or `settings`) and `key_*` files
- `--passcode`, `-p` - an optional passcode for data decryption
- `--show_settings` - show decrypted settings
- `--json`, `-j` - JSON output

### Example
```bash
$ tdesktop-decrypter /path/to/tdata -p passcode

Account 0:
MTP data:
User ID: 12345
Main DC ID: 1
Key DC 1: aabbccdd...


$ tdesktop-decrypter /path/to/tdata -p passcode -j

{
    "accounts": [
        {
            "index": 0,
            "user_id": 12345,
            "main_dc_id": 1,
            "dc_auth_keys": {
                "1": "aabbccdd..."
            }
        }
    ],
    "settings": null
}
```

## Todo (not yet implemented)
- Media decryption
- Decode `dbiApplicationSettings` setting block

## Useful links
- https://github.com/atilaromero/telegram-desktop-decrypt

- https://github.com/MihaZupan/TelegramStorageParser
