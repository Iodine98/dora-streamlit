import streamlit as st
from typing import Any
from streamlit_cookies_manager import CookieManager
from streamlit_mods.helpers.message_type import Message, BotMessage, Role
from streamlit_mods.endpoints import Endpoints


class MessageHelper:
    def __init__(self, cookie_manager: CookieManager) -> None:
        self.cookie_manager = cookie_manager
        st.session_state.messages = self.messages

    @property
    def messages(self) -> list[Message]:
        if "messages" in st.session_state:
            return st.session_state.messages
        return []

    @messages.setter
    def messages(self, value: list[Message]) -> None:
        st.session_state.messages = value

    def load_messages_from_backend(self, session_id: str) -> None:
        if (chat_history := Endpoints.get_chat_history(self.cookie_manager, session_id)) is not None:
            formatted_messages: list[Message] = []
            for message in chat_history:
                role: Role = message["type"]
                message_data = message["data"]
                content = message_data["content"]
                if "additional_kwargs" in message_data and "citations" in message_data["additional_kwargs"]:
                    citations = message_data["additional_kwargs"]["citations"]["citations"]
                else:
                    citations = []
                if role == "human":
                    formatted_messages.append(Message(role=message["type"], content=message["data"]["content"]))
                else:
                    formatted_messages.append(BotMessage(
                        role=role,
                        content=content,
                        citations=citations,
                        time=-1))
            st.session_state.messages = formatted_messages

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
