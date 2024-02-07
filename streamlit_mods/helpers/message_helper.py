import streamlit as st
from typing import Any, Literal, TypedDict
from streamlit_cookies_manager import CookieManager

from streamlit_mods.endpoints import Endpoints

class Message(TypedDict):
    role: Literal["human"] | Literal["ai"]
    content: str


class BotMessage(Message):
    content: str
    citations: list[dict[str, str]]
    time: float
    


class MessageHelper:
    def __init__(self, cookie_manager: CookieManager) -> None:
        self.cookie_manager = cookie_manager
        self.session_id = st.session_state.sessionId
        st.session_state.messages = self.messages

    @property
    def messages(self) -> list[Message]:
        if "messages" in st.session_state:
            return st.session_state.messages
        # if (message_result := Endpoints.get_chat_history(self.cookie_manager, self.session_id)) is not None:
        #     return message_result
        return []

    @messages.setter
    def messages(self, value: list[Message]) -> None:
        st.session_state.messages = value

    def get_last_message(self) -> dict[str, Any] | None:
        if len(st.session_state.messages) == 0:
            return None
        return st.session_state.messages[-1]

    def add_bot_message(self, content: str, citations: list[dict[str, str]], time: float) -> None:
        self.messages = [
            *self.messages,
            BotMessage(role="ai", content=content, citations=citations, time=time),
        ]

    def add_user_message(self, content: str) -> None:
        self.messages = [
            *self.messages,
            Message(role="human", content=content),
        ]

    @staticmethod
    def is_message_prompt(message: dict[str, Any]) -> bool:
        """
        Validating if a message counts as a human prompt.
        Only if:
        1) The role of the message (i.e. the sender) is 'human'
        2) 'content' exists as an attribute of message
        3) The message content is a string
        4) The message content is not empty
        """
        return (
            message is not None
            and message["role"] == "human"
            and "content" in message
            and isinstance(message["content"], str)
            and message["content"] != ""
        )
