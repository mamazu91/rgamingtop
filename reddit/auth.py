from base_logger import logger
import requests


def get_access_token(app_id: str, app_secret: str) -> str | None:
    logger.info('===================================================================')
    logger.info('Starting new log')
    logger.info('Authenticating to Reddit')

    if not (app_id and app_secret):
        logger.error('Could not find environment variables with Reddit app_id or app_secret')
        return None

    get_access_token_api_url = 'https://www.reddit.com/api/v1/access_token'
    get_access_token_api_data = {'grant_type': 'client_credentials'}
    get_access_token_api_headers = {'user-agent': 'rgamingtop by mamazu'}

    get_access_token_api_response = requests.post(
        url=get_access_token_api_url,
        auth=(app_id, app_secret),
        data=get_access_token_api_data,
        headers=get_access_token_api_headers
    )

    if get_access_token_api_response.status_code != 200:
        logger.error('Authentication failed')
        logger.error(f'Status code: {get_access_token_api_response.status_code}')
        return None

    logger.info('Authentication succeeded')
    return get_access_token_api_response.json()['access_token']
