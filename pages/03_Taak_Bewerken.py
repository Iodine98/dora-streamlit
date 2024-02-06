
from streamlit_mods.components.text_edit_screen.text_edit_screen import EditTaskScreen
from streamlit_mods.helpers.session_state_helper import SessionStateHelper


def main() -> None:
    session_state_helper = SessionStateHelper()
    EditTaskScreen(session_state_helper)

main()