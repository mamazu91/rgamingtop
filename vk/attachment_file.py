from base_logger import logger
import requests
from .config import HEADERS
import os


def attachment_to_file(attachment_url: str) -> str | None:
    logger.info(f'Getting Reddit attachment "{attachment_url}"')
    get_attachment_response = requests.get(
        url=attachment_url,
        headers=HEADERS
    )

    if get_attachment_response.status_code != 200:
        logger.error('Failed to get the attachment')
        logger.error(f'Status code: {get_attachment_response.status_code}')
        return None

    logger.info('Successfully got the attachment')

    logger.info('Saving it to a file')
    attachment_file_name = os.path.basename(attachment_url)
    with open(attachment_file_name, 'wb') as attachment_file:
        attachment_file.write(get_attachment_response.content)

    logger.info(f'Successfully saved it to file "{attachment_file_name}"')
    return attachment_file_name


def delete_attachment_file(attachment_file_name: str) -> None:
    logger.info(f'Deleting attachment file "{attachment_file_name}"')
    os.remove(attachment_file_name)
    logger.info('Successfully deleted the file')
