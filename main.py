import dotenv
import argparse
import logging
import json

from blockfrost import get_assets
from blockfrost import get_metadata

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
dotenv.load_dotenv('.env')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CNFT Metadata Compiler')
    parser.add_argument('--policy', help='Policy ID', required=True, type=str)
    parser.add_argument('--output', help='Output fp', required=True, type=str)
    args = vars(parser.parse_args())

    policy_id = args['policy'].lower()

    logger.info(f'Compiling metadata for policy {policy_id}')

    assets = get_assets(policy_id)

    logging.info(f'{len(assets)} assets found')

    metadata = {}

    for idx, asset in enumerate(assets):
        logging.debug(f'[{idx}/{len(assets)}] Processing {asset}')
        token_metadata = get_metadata(asset)
        metadata.update({asset: token_metadata})

    with open(args['output'], 'w') as f:
        json.dump(metadata, f, indent=4)
        f.close()