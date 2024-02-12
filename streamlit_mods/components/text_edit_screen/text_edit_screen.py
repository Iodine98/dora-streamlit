from altair import cast
import streamlit as st
from streamlit_cookies_manager import CookieManager
from streamlit_mods.components.miscellaneous import Miscellaneous
from streamlit_mods.endpoints import Endpoints
from streamlit_mods.helpers.message_helper import BotMessage

from streamlit_mods.helpers.session_state_helper import SessionStateHelper



class EditTaskScreen:
    def send_final_answer(self) -> None:
            result: bool = Endpoints.send_final_answer(cast(BotMessage, self.session_state_helper.chosen_answer), self.session_state_helper.cookie_manager, self.session_state_helper.sessionId)
            if result:
                st.success("Antwoord succesvol verstuurd! U kunt nu de applicatie afsluiten.", icon="✅")
            else:
                st.error("Er ging iets mis bij het versturen van het antwoord.", icon="❌")

    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        self.session_state_helper = session_state_helper
        if not self.session_state_helper.authenticated:
            st.error("U bent niet ingelogd.")
            st.stop()
        if self.session_state_helper.chosen_answer is None:
            st.error("U heeft nog geen antwoord gekozen.")
            st.stop()
        st.header("Bewerk hier uw antword 📝")
        txt_area_output = st.text_area("Antwoord", value=self.session_state_helper.chosen_answer["content"])
        Miscellaneous(self.session_state_helper).display_ai_message(
            content=txt_area_output,
            citations=self.session_state_helper.chosen_answer["citations"],
            time_elapsed=self.session_state_helper.chosen_answer["time"],
        )
        self.session_state_helper.chosen_answer["role"] = "final"
        self.session_state_helper.chosen_answer["content"] = txt_area_output
        st.button("Verstuur jouw eind-antwoord", key="send_edited_answer", on_click=self.send_final_answer)


        


