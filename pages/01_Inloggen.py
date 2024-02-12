from streamlit_mods.components.login_screen.login_screen import LoginScreen
from streamlit_mods.helpers.session_state_helper import SessionStateHelper


def main() -> None:
    session_state_helper = SessionStateHelper()
    LoginScreen(session_state_helper)

main()