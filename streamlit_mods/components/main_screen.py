import base64
from streamlit_mods.helpers.session_state_helper import SessionStateHelper
from streamlit_mods.endpoints import Endpoints, Result
from streamlit_mods.helpers.file_helper import FileState
from typing import Any, cast
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile
from timeit import default_timer
import time

def format_time_str(time_elapsed: float) -> str:
    if time_elapsed == 0:
        return ""
    elif time_elapsed > 100:
        return f"{round((time_elapsed)/60)} minuten"
    else:
        return f"{round(time_elapsed)} seconden"




class MainScreen:
    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        self.session_state_helper = session_state_helper
        self.file_helper = session_state_helper.file_helper
        self.message_helper = session_state_helper.message_helper
        self.init_message_content = "Hallo, ik ben DoRA. Wat kan ik voor je doen?"
        self.init()

    def display_ai_message(self, content: str, citations: list[dict[str, str]], time_elapsed: float, placeholder: DeltaGenerator | None = None) -> None:
        if placeholder:
            placeholder.markdown(content)
        else:
            st.markdown(content)
        if citations:
            self.display_citations(citations)
        if time_elapsed >= 0:
            time_str = format_time_str(time_elapsed)
            st.write(f":orange[Responstijd: {time_str}]")

    def get_file_state_by_name(self, filename: str) -> FileState:
        [file_state] = [file_state for file_state in self.file_helper.file_states if str(file_state["name"]).replace(" ", "_") == filename]
        if file_state is None:
            st.error(f"File state was not found for {filename}")
            raise ValueError(f"File state was not found for {filename}")
        return file_state

    def get_file_url(self, current_file: UploadedFile, page_number: int) -> str:
        file_bytes = current_file.getvalue()
        base64_bytes = base64.b64encode(file_bytes)
        base64_string = base64_bytes.decode()
        if current_file.type == 'application/pdf':
            return f"data:application/pdf;base64,{base64_string}#page={page_number}"
        return f"data:application/octet-stream;base64,{base64_string}"
    
    def get_file_state_html(self, file_state: FileState, page_number: int) -> str:
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
        



    def display_citations(self, citations: list[dict[str, str]]) -> None:
        source_name_html_map = {}
        for i, citation in enumerate(citations):
            with st.expander(f"Bron {i+1}"):
                if citation["source"] not in source_name_html_map:
                    current_file_state = self.get_file_state_by_name(citation["source"])
                    html_output = self.get_file_state_html(current_file_state, int(citation["page"]))
                    source_name_html_map[citation["source"]] = html_output
                file_state_html = source_name_html_map[citation["source"]]
                st.markdown(f'Bestand: {file_state_html}', unsafe_allow_html=True)
                st.markdown(f'Rangorde: {citation["ranking"]}')
                if "score" in citation and int(citation["score"]) >= 0.0:
                    st.markdown(f'Score: {round(float(citation["score"]), 2)}')
                st.markdown(f'Pagina: {citation["page"]}')
                st.markdown(f'Citaat: "{citation["proof"]}"')

    def init(self):
        if not self.session_state_helper.authenticated:
            st.stop()
        self.add_initial_message()
        self.init_chat_input()
        self.display_messages()
        self.send_prompt_on_last_message()

    def display_messages(self):
        for message in self.message_helper.messages:
            if message["role"] == "human":
                with st.chat_message("human"):
                    st.markdown(message["content"])
            elif message["role"] == "ai":
                with st.chat_message("ai"):
                    self.display_ai_message(
                        content=message["content"],
                        citations=message["citations"],
                        time_elapsed=message["time"]
                    )

    def equals_init_message(self, message: dict[str, Any]) -> bool:
        return message["content"] == self.init_message_content

    def add_initial_message(self):
        if not self.session_state_helper.initialized:
            self.message_helper.add_bot_message(self.init_message_content, [], [], -1)
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
                self.prepare_answer(*result, start)

    def prepare_answer(self, answer: str, citations: list[dict[str, str]], source_documents: Any, start_time: float):
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
        self.message_helper.add_bot_message(answer, citations, source_documents, time_elapsed)
        self.display_ai_message(full_answer, citations, time_elapsed, placeholder)
