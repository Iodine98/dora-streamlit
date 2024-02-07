import re
import streamlit as st

from streamlit_mods.helpers.session_state_helper import SessionStateHelper

def is_valid_uuid(uuid_string):
    regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    match = re.fullmatch(regex, uuid_string.lower())
    return bool(match)

class LoginScreen:
    def __init__(self, session_state_helper: SessionStateHelper) -> None:
        st.header("Inloggen 🗝️")
        uuid_value = st.text_input(
            label="UUID", 
            value=session_state_helper.sessionId,
            key="login_screen_uuid_input",
            placeholder="Vul hier uw UUID in.",
            max_chars=36)
        if is_valid_uuid(uuid_value):
            st.success("UUID is geldig.", icon="✅")
            session_state_helper.sessionId = uuid_value
            session_state_helper.authenticated = True
            session_state_helper.message_helper.load_messages_from_backend(session_state_helper.sessionId)
        else:
            if uuid_value == "":
                st.warning("Vul uw UUID hierboven in.")
            else:
                st.error("UUID is ongeldig. Probeer het opnieuw.", icon="❌")
            session_state_helper.sessionId = uuid_value
            session_state_helper.authenticated = False

        