from streamlit_mods.components.chat_screen.sidebar import Sidebar
from streamlit_mods.components.chat_screen.chat_screen import ChatScreen
from .helpers.session_state_helper import SessionStateHelper
import streamlit as st
from .endpoints import Endpoints
from typing import Any


class AppLayout:
    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        st.title("DoRA Chatbot")
        st.subheader("Documenten Raadplegen en Analyseren")
        self.session_state_helper = session_state_helper
        self.message_helper = session_state_helper.message_helper
        self.file_helper = session_state_helper.file_helper
        st.markdown("Welkom bij de DoRA Chatbot. Hier kun je documenten raadplegen en analyseren. Om te beginnen, klik op de knop 'Inloggen' in de sidebar.")
        

    def identify(self):
        json_response: dict[str, Any] | None = Endpoints.identify(
            self.session_state_helper.cookie_manager, session_id=self.session_state_helper.session_id
        )
        if json_response is None:
            return
        self.session_state_helper.authenticated = json_response["authenticated"]
        self.session_state_helper.session_id = json_response["sessionId"]

    def initialize_sidebar(self):
        Sidebar(self.session_state_helper)

    def initialize_main(self):
        ChatScreen(self.session_state_helper)
