from reddit.main import get_top_post
from vk.main import make_post
import time


def main() -> None:
    while True:
        reddit_top_post = get_top_post()

        if not reddit_top_post:
            return None

        make_post(reddit_top_post)

        time.sleep(3600)


if __name__ == '__main__':
    main()
