from .decrypter import TdataReader

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('tdata', type=str, help='Path to tdata/ directory')
    args = parser.parse_args()

    reader = TdataReader(args.tdata)
    parsed_tdata = reader.read()

    for account in parsed_tdata.accounts.values():
        print(f'Account {account.index}:')

        print('MTP data:')
        print(f'User ID: {account.mtp_data.user_id}')
        print(f'Main DC ID: {account.mtp_data.current_dc_id}')

        for dc_id, key in account.mtp_data.keys.items():
            print(f'Key DC {dc_id}: {key.hex(" ")}')