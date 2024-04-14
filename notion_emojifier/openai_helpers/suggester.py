import logging
from typing import cast

from emoji import emoji_list
from openai import OpenAI

INSTRUCTIONS = """
You predict the best emoji for task titles in a notion database.
 The database is for a robotics company that builds lumber processing robots.
 The company focuses on automating the process of removing nails from lumber,
 allowing wood to be easily salvaged. Tasks can range from high level software or
 mechanical engineering to low level tasks like cleaning the shop or organizing parts.

When choosing an emoji, try to be creative, punny, and interesting. Don't choose
 emojis that are generic- for example, don't use the robot emoji for a robotics
 related task. Try to use an emoji reflective of the task content itself.
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
    def __init__(self, client: OpenAI):
        self._client = client

    def suggest_emoji(self, title: str, tries: int = 0, max_tries: int = 5) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-4",
            messages=[
                *PREAMBLE_MESSAGES,  # type: ignore
                {"role": "user", "content": f"Title: {title}"},
            ],
        )
        prediction = cast(str, completion.choices[0].message.content)
        emojis = cast(list[str], [e["emoji"] for e in emoji_list(prediction)])

        if len(emojis) != 1:
            if tries >= max_tries:
                raise EmojiPredictionFailed(
                    f"Failed to suggest emoji for title: {title}"
                )

            logging.warning(
                f"Invalid response: {prediction} for title {title}. Retrying..."
            )
            return self.suggest_emoji(title, tries + 1, max_tries=max_tries)
        return emojis[0]
