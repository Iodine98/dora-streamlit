from typing import cast
import streamlit as st
from streamlit_mods.helpers.file_helper import FileState
from streamlit_mods.helpers.message_helper import BotMessage
from streamlit_mods.helpers.session_state_helper import SessionStateHelper
from streamlit.delta_generator import DeltaGenerator

def format_time_str(time_elapsed: float) -> str:
        if time_elapsed == 0:
            return ""
        elif time_elapsed > 100:
            return f"{round((time_elapsed)/60)} minuten"
        else:
            return f"{round(time_elapsed)} seconden"

class Miscellaneous:
    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        self.session_state_helper = session_state_helper
        self.message_helper = session_state_helper.message_helper
        self.file_helper = session_state_helper.file_helper

    

    def display_ai_message(self, content: str, citations: list[dict[str, str]], time_elapsed: float, placeholder: DeltaGenerator | None = None, counter: int = -1) -> None:
        def message_selected_on_click() -> None:
            self.session_state_helper.chosen_answer = cast(BotMessage, self.message_helper.messages[counter])
            st.toast("U heeft uw antwoord gekozen! Nu kunt u op 'Taak Bewerken' klikken om uw antwoord te bewerken.", icon="✅")
        if placeholder:
            placeholder.markdown(content)
        else:
            st.markdown(content)
        if counter >= 0:
            st.button("Kies dit antwoord", key="choose_answer " + str(counter), on_click=message_selected_on_click)
        if citations:
            self.display_citations(citations, counter)
        if time_elapsed >= 0:
            time_str = format_time_str(time_elapsed)
            st.write(f":orange[Responstijd: {time_str}]")

    def get_file_state_by_name(self, filename: str) -> FileState | None:
        matching_file_states = [file_state for file_state in self.file_helper.file_states if str(file_state["name"]).replace(" ", "_") == filename]
        if not matching_file_states:
            return None
        return matching_file_states[0]

    def display_citations(self, citations: list[dict[str, str]], message_counter: int) -> None:
        for i, citation in enumerate(citations):
            with st.expander(f"Bron {i+1}"):
                current_file_state = self.get_file_state_by_name(citation["source"])
                col1, col2 = st.columns([1,7], gap="small")
                col1.markdown("Bestand:")
                if current_file_state is None:
                    col2.markdown(f"{citation['source']}")
                else:
                    col2.download_button(
                        label=f"{current_file_state['name']}",
                        data=current_file_state["file"],
                        file_name=current_file_state["name"],
                        mime="application/octet-stream",
                        key=f"{citation['source'], i, message_counter}"
                    )
                st.markdown(f'Rangorde: {citation["ranking"]}')
                if "score" in citation and int(citation["score"]) >= 0.0:
                    st.markdown(f'Score: {round(float(citation["score"]), 2)}')
                st.markdown(f'Pagina: {citation["page"]}')
                st.markdown(f'''Citaat: "*{citation["proof"]}*"''')
        