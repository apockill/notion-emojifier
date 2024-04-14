from typing import Any, Literal

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
        try:
            title_property = self.properties[self.title_property_name]
        except KeyError as e:
            raise ValueError(
                "The 'Name' property for this page was not found. It's possible this "
                "database has a non-default title property name. Please specify the "
                "title property name in the 'title-property-name' script argument."
            ) from e

        if not isinstance(title_property, Name):
            raise ValueError(
                f"Expected the title property to contain information about the title "
                f"of the page, but got {title_property}. Please make sure the title "
                f"property is a 'Name' property, or override the 'title-property-name'"
                f" script argument to point to the correct title property."
            )
        return title_property.title[0].plain_text
