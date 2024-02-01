from streamlit_mods.components.login_screen.login_screen import LoginScreen
from streamlit_mods.components.chat_screen.chat_screen import ChatScreen
from streamlit_mods.helpers.session_state_helper import SessionStateHelper


def main() -> None:
    session_state_helper = SessionStateHelper()
    LoginScreen(session_state_helper)

main()
