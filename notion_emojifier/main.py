import logging
import os
from argparse import ArgumentParser
from pathlib import Path

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
    parser.add_argument(
        "--backup-file",
        default=Path("emoji_backup.txt"),
        type=Path,
        help="File to save the ID's of pages that were edited",
    )
    args = parser.parse_args()

    openai = OpenAI(api_key=args.openai_key)
    notion = Client(auth=args.notion_key)

    # Create helpers
    pages = notion_helpers.DatabasePageIterator(
        notion=notion, database_id=args.database_id
    )
    emoji_updater = notion_helpers.PageEmojiEditor(
        client=notion, backup_file=args.backup_file, allow_overwrite=False
    )
    emojifier = openai_helpers.TitleEmojifier(client=openai)

    # Apply emojis to pages
    for i, page in enumerate(pages):
        if page.icon is not None:
            logging.info(f"Emoji already exists for page '{page.url}'. Skipping...")
            continue

        emoji = emojifier.suggest_emoji(page.title)

        logging.info(f"Applying emoji {emoji} to page '{page.title}', {page.url}")
        emoji_updater.apply_emoji(emoji, page)
        if i > 1:
            break


if __name__ == "__main__":
    main()
