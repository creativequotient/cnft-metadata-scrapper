import requests
import logging
import json
import dotenv
import os

from utils import redis

logger = logging.getLogger(__name__)
dotenv.load_dotenv('.env')

BLOCKFROST_HEADER = {
    'project_id': os.getenv('BLOCKFROST_PROJECT_ID')
}

def get_assets(policy_id):
    '''Return a list of all assets under a given policy_id'''

    base_url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'

    page_num = 1

    assets = []

    while True:
        url = f'{base_url}?page={page_num}&order=desc'
        req = requests.get(url, headers=BLOCKFROST_HEADER, timeout=3)

        if req.status_code != 200:
            return None

        page_assets = req.json()

        for pg_asset in page_assets:
            if int(pg_asset['quantity']) > 0:
                assets.append(pg_asset['asset'])

        if len(page_assets) < 100:
            break

        page_num += 1

    return assets

def get_metadata(asset):
    '''Return metadata given asset'''

    redisKey = f'metadata:{asset}'

    cacheResult = redis.get(redisKey)

    if cacheResult:
        logging.debug(f'Cached value for {asset} found')
        return json.loads(cacheResult)

    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset}'

    req = requests.get(url, headers=BLOCKFROST_HEADER, timeout=3)

    if req.status_code != 200:
        return None

    result = req.json()

    metadata = result['onchain_metadata']

    redis.setex(redisKey, 60 * 60 * 24, json.dumps(metadata))

    return metadata