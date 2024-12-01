# Telegram Desktop tdata decrypter
Inspired by [telegram-desktop-decrypt](https://github.com/atilaromero/telegram-desktop-decrypt)

## Features
- Accounts MTP auth data decryption (User ID, DC ID, DC keys)
- Settings decryption

## Installation
```bash
git clone https://github.com/ntqbit/tdesktop-decrypter
pip install ./tdesktop-decrypter
```

## Usage
### Arguments
- `tdata` - path to tdata folder containing `settings` (or `settings`) and `key_*` files
- `--passcode`, `-p` - an optional passcode for data decryption
- `--show_settings` - show decrypted settings

### Example
```bash
$ python -m tdesktop_decrypter /path/to/tdata -p helloworld

Account 0:
MTP data:
User ID: 12345
Main DC ID: 1
Key DC 1: AA BB CC DD ...
```

## Todo (not yet implemented)
- Media decryption

## Useful links
- https://github.com/atilaromero/telegram-desktop-decrypt

- https://github.com/MihaZupan/TelegramStorageParser
