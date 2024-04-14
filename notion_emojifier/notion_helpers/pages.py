import logging
from pathlib import Path

from notion_client import Client

from .schemas import Icon, Page


class PageEmojiEditor:
    def __init__(
        self,
        client: Client,
        backup_file: Path = Path("emoji_backup.txt"),
        allow_overwrite: bool = False,
    ):
        """A helper for editing page emojis in Notion.
        :param client: The Notion API client
        :param backup_file: A file to save the ID's of pages that were edited, along
            with what emoji was added
        :param allow_overwrite: Whether to allow overwriting the emoji if one already
            exists.
        """
        self._client = client
        self._backup_file = backup_file
        self._allow_overwrite = allow_overwrite

    def apply_emoji(self, emoji: str, page: Page) -> bool:
        """Apply an emoji to a page.
        :param emoji: The emoji to apply
        :param page: The page to apply the emoji to
        :return: True if the emoji was applied, False if not
        """
        if page.icon is not None and not self._allow_overwrite:
            logging.info(f"Emoji already exists for page '{page.title}'. Skipping...")
            return False

        new_icon = Icon(type="emoji", emoji=emoji).to_dict()
        self._client.pages.update(icon=new_icon, page_id=page.id)

        # Record the change in the backup file
        with self._backup_file.open("a") as f:
            f.write(f"{page.id}: {emoji}\n")
        return True
