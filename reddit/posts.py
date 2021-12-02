from .config import PREVIOUS_POSTS_FILENAME
from base_logger import logger
import requests


def get_current_posts(access_token: str) -> list | None:
    if not access_token:
        return None

    get_current_posts_api_url = 'https://oauth.reddit.com/r/gaming/top/'
    get_current_posts_api_headers = {
        'Authorization': f'bearer {access_token}',
        'user-agent': 'rgamingtop by mamazu'
    }
    get_current_posts_api_params = {
        't': 'hour',
        'limit': 24
    }

    logger.info('Getting last 24 posts')
    get_current_posts_response = requests.get(
        url=get_current_posts_api_url,
        headers=get_current_posts_api_headers,
        params=get_current_posts_api_params
    )

    if get_current_posts_response.status_code != 200:
        logger.error('Failed to get the posts')
        logger.error(f'Status code: {get_current_posts_response.status_code}')
        return None

    logger.info('Successfully got the posts')
    return get_current_posts_response.json()['data']['children']


def read_previous_posts() -> list:
    logger.info('Opening the file with previous posts')
    with open(PREVIOUS_POSTS_FILENAME, 'r+', encoding='utf-8') as previous_posts_file:
        previous_posts_urls = []
        logger.info('Found the following posts:')
        for index, previous_post_url in enumerate(previous_posts_file.readlines()):
            logger.info(f'{index + 1}: "{previous_post_url.strip()}"')
            previous_posts_urls.append(previous_post_url.strip())

    return previous_posts_urls


def previous_posts_file_cleanup(previous_posts: list) -> None:
    if len(previous_posts) > 24:
        logger.info('The file already contains 24 posts, deleting the oldest one')
        previous_posts.pop(0)
        logger.info('Successfully deleted the item')
        logger.info('Updated list of posts:')
        for index, previous_post in enumerate(previous_posts):
            logger.info(f'{index + 1}: "{previous_post}"')

    logger.info('Saving the updated list of posts to the file')
    with open('previous_posts.log', 'w', encoding='utf-8') as previous_posts_file:
        previous_posts_file.write('\n'.join(previous_posts))
    logger.info('Successfully saved the list')


def select_top_post(current_posts: list, previous_posts: list) -> dict | None:
    logger.info('Selecting the top post')
    for index, top_post in enumerate(current_posts):
        top_post_url = 'https://reddit.com' + top_post['data']['permalink']
        logger.info(f'Checking post [{index + 1}]: "{top_post_url}"')

        logger.info('Contains an attachment?')
        if 'post_hint' in top_post['data']:
            logger.info('> Yes')

            logger.info('Is the post unique?')
            if top_post_url not in previous_posts:
                logger.info('> Yes')

                logger.info('Is attachment an image?')
                if top_post['data']['post_hint'] == 'image':
                    logger.info('> Yes')
                    previous_posts.append(top_post_url)
                    break

        logger.info('> No, continuing with another post')
        continue
    else:
        logger.error('Did not manage to find a top post (ran out of posts)')
        return None

    logger.info('Successfully found the top post')
    return top_post
