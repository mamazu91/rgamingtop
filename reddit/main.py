from .auth import get_access_token
from .config import APP_ID, APP_SECRET
from .posts import get_current_posts, read_previous_posts, select_top_post, previous_posts_file_cleanup
from base_logger import logger


def get_top_post() -> dict | None:
    access_token = get_access_token(APP_ID, APP_SECRET)

    current_posts = get_current_posts(access_token)

    if not current_posts:
        return None

    previous_posts = read_previous_posts()
    top_post = select_top_post(current_posts, previous_posts)
    previous_posts_file_cleanup(previous_posts)

    if not top_post:
        return None

    top_post_url = 'https://reddit.com' + top_post['data']['permalink']
    top_post_title = top_post['data']['title']
    top_post_attachment_url = top_post['data']['url']

    logger.info('Returning the following data on the selected top post:')
    logger.info(f'URL: "{top_post_url}"')
    logger.info(f'Title: "{top_post_title}"')
    logger.info(f'Attachment URL: "{top_post_attachment_url}"')
    return {
        'top_post_url': top_post_url,
        'top_post_title': top_post_title,
        'top_post_attachment_url': top_post_attachment_url
    }
