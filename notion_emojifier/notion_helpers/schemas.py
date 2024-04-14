from typing import Literal, Any

from openai import BaseModel


class NoPageTitle(Exception):
    pass


class Icon(BaseModel):
    type: Literal["emoji"]
    emoji: str


class Title(BaseModel):
    plain_text: str


class Name(BaseModel):
    title: list[Title]


class Page(BaseModel):
    id: str
    icon: None | Icon
    url: str
    properties: dict[str, Name | dict[Any, Any]]
    in_trash: bool
    title_property_name: str

    @property
    def title(self) -> str:
        return self.properties[self.title_property_name].title[0].plain_text
