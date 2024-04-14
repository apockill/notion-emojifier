from collections.abc import Iterator
from typing import Any

from notion_client import Client

from .schemas import Page


class DatabasePageIterator:
    def __init__(self, notion: Client, database_id: str, title_property_name: str):
        self._client = notion
        self._database_id = database_id
        self._title_property_name = title_property_name

    def __iter__(self) -> Iterator[Page]:
        start_cursor = None
        while True:
            response: Any
            response = self._client.databases.query(
                database_id=self._database_id, start_cursor=start_cursor
            )
            for result in response["results"]:
                yield Page(**result, title_property_name=self._title_property_name)

            # Notion API provides a 'next_cursor' if there are more pages to fetch
            if response["has_more"]:
                start_cursor = response["next_cursor"]
            else:
                break
