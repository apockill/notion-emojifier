from typing import Literal

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


class PageProperties(BaseModel):
    Name: Name


class Page(BaseModel):
    id: str
    icon: None | Icon
    url: str
    properties: PageProperties
    in_trash: bool

    @property
    def title(self) -> str:
        if not self.properties.Name.title:
            raise NoPageTitle(f"Page {self.id} has no title")
        return self.properties.Name.title[0].plain_text
