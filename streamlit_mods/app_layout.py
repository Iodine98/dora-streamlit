from streamlit_mods.components.chat_screen.sidebar import Sidebar
from streamlit_mods.components.chat_screen.chat_screen import ChatScreen
from streamlit_mods.components.login_screen.login_screen import LoginScreen
from .helpers.session_state_helper import SessionStateHelper
from .endpoints import Endpoints, Result
from typing import Any
import streamlit as st


class AppLayout:
    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        st.title("DoRA Chatbot")
        st.subheader("Documenten Raadplegen en Analyseren")
        self.session_state_helper = session_state_helper
        self.message_helper = session_state_helper.message_helper
        self.file_helper = session_state_helper.file_helper
        st.markdown("Welkom bij de DoRA Chatbot. Hier kun je documenten raadplegen en analyseren. Om te beginnen, klik op de knop 'Inloggen' in de sidebar.")
        

    # def identify(self):
    #     json_response: dict[str, Any] | None = Endpoints.identify(
    #         self.session_state_helper.cookie_manager, session_id=self.session_state_helper.sessionId
    #     )
    #     if json_response is None:
    #         return
    #     self.session_state_helper.authenticated = json_response["authenticated"]
    #     self.session_state_helper.sessionId = json_response["sessionId"]
