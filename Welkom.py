from streamlit_mods import SessionStateHelper, AppLayout


def main():
    session_state_helper = SessionStateHelper()
    AppLayout(session_state_helper)


if __name__ == "__main__":
    main()
