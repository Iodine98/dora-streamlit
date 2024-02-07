from streamlit_mods import SessionStateHelper, AppLayout


def main():
    session_state_helper = SessionStateHelper()
    app_layout = AppLayout(session_state_helper)
    app_layout.initialize_sidebar()
    app_layout.initialize_main()


if __name__ == "__main__":
    main()
