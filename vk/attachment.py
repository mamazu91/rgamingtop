from base_logger import logger
import requests
from vk.config import HEADERS, GROUP_ID, ACCESS_TOKEN, API_VERSION


def get_attachment_upload_url() -> str | None:
    get_attachment_upload_url_api_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    get_attachment_upload_url_params = {
        'group_id': GROUP_ID,
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION
    }

    logger.info('Getting URL for attachment upload')
    get_attachment_upload_link_response = requests.get(
        url=get_attachment_upload_url_api_url,
        headers=HEADERS,
        params=get_attachment_upload_url_params
    )

    get_attachment_upload_link_response_json = get_attachment_upload_link_response.json()

    if 'error' in get_attachment_upload_link_response_json:
        logger.error('Failed to get the URL')
        logger.error(f'Error: {get_attachment_upload_link_response_json}')
        return None

    logger.info('Successfully got the URL')
    return get_attachment_upload_link_response_json['response']['upload_url']


def upload_attachment(attachment_filename: str) -> dict | None:
    attachment_upload_url = get_attachment_upload_url()

    if not attachment_upload_url:
        return None

    logger.info('Uploading the attachment to VK')
    try:
        with open(attachment_filename, 'rb') as attachment_file:
            upload_attachment_api_response = requests.post(
                url=attachment_upload_url,
                files={'photo': attachment_file},
                headers=HEADERS
            )
    except FileNotFoundError:
        logger.error(f'Could not find the attachment "{attachment_filename}" on disk')
        return None

    upload_attachment_api_response_json = upload_attachment_api_response.json()

    if 'error' in upload_attachment_api_response_json:
        logger.error('Failed to upload the attachment')
        logger.error(f'Error: {upload_attachment_api_response_json}')
        return None

    if upload_attachment_api_response_json['photo'] == '[]':
        logger.error('Failed to upload the attachment')
        logger.error('Got empty photo list back from VK')
        return None

    logger.info('Successfully uploaded the attachment')
    return upload_attachment_api_response_json


def save_attachment_to_wall(uploaded_attachment_metadata: dict) -> dict | None:
    logger.info('Saving the attachment to wall')
    save_wall_photo_api_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': GROUP_ID,
        'photo': uploaded_attachment_metadata['photo'],
        'server': uploaded_attachment_metadata['server'],
        'hash': uploaded_attachment_metadata['hash'],
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION
    }

    save_wall_photo_api_response = requests.get(
        url=save_wall_photo_api_url,
        headers=HEADERS,
        params=params
    )

    save_wall_photo_api_response_json = save_wall_photo_api_response.json()

    if 'error' in save_wall_photo_api_response_json:
        logger.error('Failed to save the attachment')
        logger.error(f'Error: {save_wall_photo_api_response_json}')
        return None

    logger.info('Successfully saved the attachment')

    vk_attachment_id = save_wall_photo_api_response_json['response'][0]['id']
    vk_attachment_owner_id = save_wall_photo_api_response_json['response'][0]['owner_id']
    return {
        'id': vk_attachment_id,
        'owner_id': vk_attachment_owner_id
    }
