import logging
from typing import cast

from emoji import emoji_list
from openai import OpenAI

INSTRUCTIONS = """
You predict the best emoji for task titles in a notion database.

About this database:
> {database_description}

When choosing an emoji, try to be creative, punny, and interesting. Don't choose
 emojis that are generic- for example, don't use the robot emoji for a robotics
 related task. Try to use an emoji reflective of the task content itself.
 Return only 1 emoji per task title.
"""


PREAMBLE_MESSAGES = [
    {"role": "system", "content": INSTRUCTIONS},
    {"role": "user", "content": "Title: Get all axes homed on ACS"},
    {"role": "assistant", "content": "🏠"},
    {"role": "user", "content": "Title: Clean the shop"},
    {"role": "assistant", "content": "🧹"},
    {
        "role": "user",
        "content": "Title: Add docker to the build system",
    },
    {"role": "assistant", "content": "🐳"},
    {
        "role": "user",
        "content": "Title: Install a new gripper on left bird",
    },
    {"role": "assistant", "content": "🤏"},
    {
        "role": "user",
        "content": "Title: Organize the bits in the shop cabinet",
    },
    {"role": "assistant", "content": "🧰"},
    {"role": "user", "content": "Title: Implement a new logging system"},
    {"role": "assistant", "content": "📝"},
]


class EmojiPredictionFailed(Exception):
    pass


class TitleEmojifier:
    def __init__(self, client: OpenAI, database_description: str):
        self._client = client
        self._database_description = database_description

    def suggest_emoji(self, title: str, tries: int = 0, max_tries: int = 5) -> str:
        # Insert the database description into the preamble messages
        preamble = PREAMBLE_MESSAGES.copy()
        preamble[0]["content"] = INSTRUCTIONS.format(
            database_description=self._database_description
        )

        completion = self._client.chat.completions.create(
            model="gpt-4",
            messages=[
                *preamble,  # type: ignore
                {"role": "user", "content": f"Title: {title}"},
            ],
        )
        prediction = cast(str, completion.choices[0].message.content)
        emojis = cast(list[str], [e["emoji"] for e in emoji_list(prediction)])

        if len(emojis) == 0:
            if tries >= max_tries:
                raise EmojiPredictionFailed(
                    f"Failed to suggest emoji for title: {title}"
                )

            logging.warning(
                f"Invalid response: {prediction} for title {title}. Retrying..."
            )
            return self.suggest_emoji(title, tries + 1, max_tries=max_tries)
        return emojis[0]
