import logging
import os
from argparse import ArgumentParser
from pathlib import Path

from notion_client import Client
from openai import OpenAI

from notion_emojifier import notion_helpers, openai_helpers

EXAMPLE_DATABASE_DESCRIPTION = """
 This database holds tasks for a robotics company that builds lumber processing robots.
 The company focuses on automating the process of removing nails from lumber,
 allowing wood to be easily salvaged. Tasks can range from high level software or
 mechanical engineering to low level tasks like cleaning the shop or organizing parts.
"""


def main() -> None:
    # Logging configuration
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

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
    parser.add_argument(
        "--database-description",
        default=EXAMPLE_DATABASE_DESCRIPTION,
        help="Description of the database to be used in the OpenAI prompt",
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
    emojifier = openai_helpers.TitleEmojifier(
        client=openai, database_description=args.database_description
    )

    # Apply emojis to pages
    for page in pages:
        if page.icon is not None:
            logging.info(f"Emoji already exists for page url: {page.url}. Skipping...")
            continue

        try:
            title = page.title
        except notion_helpers.NoPageTitle:
            logging.warning(f"Page {page.id} has no title. Skipping...")
            continue

        emoji = emojifier.suggest_emoji(title)

        logging.info(f"Applying emoji {emoji} to page '{title}', url: {page.url}")
        emoji_updater.apply_emoji(emoji, page)


if __name__ == "__main__":
    main()
