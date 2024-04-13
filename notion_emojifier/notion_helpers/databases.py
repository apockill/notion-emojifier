from notion_client import Client


class DatabasePageIterator:
    def __init__(self, notion: Client, database_id: str):
        self._client = notion
        self._database_id = database_id

    def __iter__(self):
        start_cursor = None
        while True:
            response = self._client.databases.query(
                database_id=self._database_id,
                start_cursor=start_cursor
            )
            for result in response["results"]:
                yield result

            # Notion API provides a 'next_cursor' if there are more pages to fetch
            if response["has_more"]:
                start_cursor = response["next_cursor"]
            else:
                break