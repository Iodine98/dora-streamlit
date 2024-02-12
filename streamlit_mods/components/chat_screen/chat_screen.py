import base64
from streamlit_mods.components.miscellaneous import Miscellaneous
from streamlit_mods.helpers.message_helper import BotMessage
from streamlit_mods.helpers.session_state_helper import SessionStateHelper
from streamlit_mods.endpoints import Endpoints, Result
from streamlit_mods.helpers.file_helper import FileState
from typing import Any, cast
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from timeit import default_timer
import time


def get_file_state_html(file_state: FileState, page_number: int) -> str:
        current_file = file_state["file"]
        file_bytes = current_file.getvalue()
        base64_bytes = base64.b64encode(file_bytes)
        base64_string = base64_bytes.decode()
        if current_file.type == 'application/pdf':
            file_url = f"data:application/pdf;base64,{base64_string}#page={page_number}"
            return f'<a href="{file_url}" download="{file_state["name"]}" target="_blank">{file_state["name"]}</a>'

        else:
            file_url = f"data:application/octet-stream;base64,{base64_string}"
            return f'<a href="{file_url}" download="{file_state["name"]}" target="_blank">{file_state["name"]}</a>'
      



class ChatScreen:
    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        st.header("Chat met DoRA 🤖")
        st.warning("Klik NIET op 'Taak Bewerken' totdat je klaar bent met chatten. Zodra je op 'Taak Bewerken' klikt, worden de documenten die je hebt geüpload verwijderd. \
                   \n Mocht dit onverhoopt toch gebeuren, üpload de bestanden dan opnieuw.")
        self.session_state_helper = session_state_helper
        self.file_helper = session_state_helper.file_helper
        self.message_helper = session_state_helper.message_helper
        self.display_ai_message = Miscellaneous(session_state_helper).display_ai_message
        self.init_message_content = "Hallo, ik ben DoRA. Wat kan ik voor je doen?"
        if not self.session_state_helper.authenticated:
            st.error("U bent niet ingelogd.")
            st.stop()
        self.add_initial_message()
        self.init_chat_input()
        self.display_messages()
        self.send_prompt_on_last_message()
        

    def display_messages(self):
        for i, message in enumerate(self.message_helper.messages):
            if message["role"] == "human":
                with st.chat_message("human"):
                    st.markdown(message["content"])
            elif message["role"] == "ai":
                with st.chat_message("ai"):
                    message = cast(BotMessage, message)
                    self.display_ai_message(
                        content=message["content"],
                        citations=message["citations"],
                        time_elapsed=message["time"],
                        counter=i,
                    )

    def equals_init_message(self, message: dict[str, Any]) -> bool:
        return message["content"] == self.init_message_content

    def add_initial_message(self):
        if not self.session_state_helper.initialized:
            time.sleep(0.1)
            self.message_helper.add_bot_message(self.init_message_content, [], -1)
            self.session_state_helper.initialized = True

    def init_chat_input(self):
        if question := st.chat_input("Stel een vraag", key="chat_input"):
            self.message_helper.add_user_message(question)

    def send_prompt_on_last_message(self):
        last_message = self.message_helper.get_last_message()
        if last_message is None or not self.message_helper.is_message_prompt(last_message):
            return
        with st.chat_message("ai"):
            with st.spinner("Aan het denken..."):
                start = default_timer()
                result: Result | None = Endpoints.prompt(
                    self.session_state_helper.cookie_manager,
                    last_message["content"],
                    self.session_state_helper.sessionId,
                )
                if result is None:
                    st.error("Er ging iets mis bij het versturen van de vraag.")
                    return
            with st.spinner("Antwoord aan het formuleren..."):
                self.prepare_answer(*result, start_time=start)

    def prepare_answer(self, answer: str, citations: list[dict[str, str]], start_time: float):
        def build_placeholder() -> tuple[DeltaGenerator, str]:
            placeholder = st.empty()
            full_answer = ""
            for item in answer:
                full_answer += item
                placeholder.markdown(full_answer + "▌")
                time.sleep(0.1)
            return placeholder, full_answer

        placeholder, full_answer = build_placeholder()
        end = default_timer()
        time_elapsed = end - start_time
        self.message_helper.add_bot_message(content=answer, citations=citations, time=time_elapsed)
        self.display_ai_message(full_answer, citations, time_elapsed, placeholder, len(self.message_helper.messages) - 1)
