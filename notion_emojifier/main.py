import logging
import os
from argparse import ArgumentParser

from notion_client import Client

from notion_emojifier import notion_helpers

logging.basicConfig(level=logging.INFO)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--notion-key", default=os.getenv("NOTION_KEY"), help="Notion API key"
    )
    parser.add_argument(
        "--openai-key", default=os.getenv("OPENAI_KEY"), help="OpenAI API key"
    )
    parser.add_argument("--database-id", help="Notion database ID", required=True)
    args = parser.parse_args()

    notion = Client(auth=args.notion_key)

    pages = notion_helpers.DatabasePageIterator(
        notion=notion, database_id=args.database_id
    )
    for i, page in enumerate(pages):
        logging.info(page)


if __name__ == "__main__":
    main()
