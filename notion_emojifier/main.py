import logging
import os
from argparse import ArgumentParser

from notion_client import Client
from openai import OpenAI

from notion_emojifier import notion_helpers, openai_helpers

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

    openai = OpenAI(api_key=args.openai_key)

    notion = Client(auth=args.notion_key)

    pages = notion_helpers.DatabasePageIterator(
        notion=notion, database_id=args.database_id
    )
    emojifier = openai_helpers.TitleEmojifier(client=openai)

    for i, page in enumerate(pages):
        emoji = emojifier.suggest_emoji(page.title)
        logging.info(f"Emoji for '{page.title}': {emoji}")

        if i > 10:
            break


if __name__ == "__main__":
    main()
