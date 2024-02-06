from streamlit_mods.components.chat_screen.sidebar import Sidebar
from streamlit_mods.components.chat_screen.chat_screen import ChatScreen
from streamlit_mods.helpers.session_state_helper import SessionStateHelper


def main() -> None:
    session_state_helper = SessionStateHelper()
    ChatScreen(session_state_helper)
    Sidebar(session_state_helper)

main()
