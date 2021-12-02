from .config import GROUP_ID, ACCESS_TOKEN, API_VERSION, HEADERS
from base_logger import logger
from .attachment_file import attachment_to_file, delete_attachment_file
from .attachment import upload_attachment, save_attachment_to_wall
import requests


def prepare_post_metadata(reddit_top_post: dict) -> dict | None:
    attachment_file_name = attachment_to_file(reddit_top_post['top_post_attachment_url'])

    if not attachment_file_name:
        return None

    uploaded_attachment_metadata = upload_attachment(attachment_file_name)

    if not uploaded_attachment_metadata:
        return None

    post_metadata = save_attachment_to_wall(uploaded_attachment_metadata)

    if not post_metadata:
        return None

    delete_attachment_file(attachment_file_name)

    return post_metadata


def make_post(reddit_top_post: dict) -> str | None:
    post_metadata = prepare_post_metadata(reddit_top_post)

    if not post_metadata:
        return None

    id, owner_id = post_metadata.values()

    logger.info('Creating a post')
    wall_post_api_url = 'https://api.vk.com/method/wall.post'
    wall_post_api_params = {
        'owner_id': f'-{GROUP_ID}',
        'from_group': 1,
        'message': reddit_top_post['top_post_title'],
        'attachment': f"photo{owner_id}_{id},{reddit_top_post['top_post_url']}",
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION
    }
    wall_post_api_response = requests.get(
        url=wall_post_api_url,
        headers=HEADERS,
        params=wall_post_api_params
    )

    wall_post_api_response_json = wall_post_api_response.json()

    if 'error' in wall_post_api_response_json:
        logger.error('Failed to create a post')
        logger.error(f'Error: {wall_post_api_response_json}')
        return None

    logger.info('Successfully created a post')
