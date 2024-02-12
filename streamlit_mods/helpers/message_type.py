from typing import Any, Literal, TypedDict

Role = Literal["human"] | Literal["ai"] | Literal["final"]

class Message(TypedDict):
    role: Role
    content: str


class BotMessage(Message):
    content: str
    citations: list[dict[str, str]]
    time: float
    