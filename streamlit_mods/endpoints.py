import json
import os
import requests
from typing import Any
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_cookies_manager import CookieManager

from streamlit_mods.helpers.message_helper import BotMessage


Result = tuple[str, list[dict[str, str]], Any]
backend_url = os.environ.get("FLASK_URL")


class Endpoints:
    @staticmethod
    def identify(cookie_manager: CookieManager, session_id: str | None = None) -> dict[str, Any] | None:
        try:
            session_id_entry = {"sessionId": session_id} if session_id else {}
            response = requests.get(f"{backend_url}/identify", data={**session_id_entry})
            json_response = response.json()
            if json_response["error"] != "":
                st.error(json_response["error"])
                return
            response_message = json_response["message"]
            cookie_manager["sessionId"] = json_response["sessionId"]
            st.toast(response_message, icon="🤗")
            return json_response
        except Exception as err:
            st.error(err, icon="❌")

    @staticmethod
    def upload_files(
        cookie_manager: CookieManager, uploaded_files: list[UploadedFile], session_id: str | None = None
    ) -> dict[str, list[str]]:
        if not cookie_manager.ready():
            st.stop()
        prefix = "file_"
        prefix_filename = lambda name: prefix + name
        files_with_prefix = {prefix_filename(file.name): (file.name, file.read(), file.type) for file in uploaded_files}
        prefix_entry = {"prefix": prefix}
        session_id_entry = {"sessionId": session_id} if session_id else {}
        form_data = {
            **prefix_entry,
            **session_id_entry,
        }
        try:
            response = requests.post(f"{backend_url}/upload_files", data=form_data, files=files_with_prefix)
            json_response = response.json()
            if json_response["error"] != "":
                raise Exception(json_response["error"])
            response_message = json_response["message"]
            st.toast(response_message, icon="✅")
            return json_response["fileIdMapping"]
        except Exception as err:
            st.error(err, icon="❌")
        return {}

    @staticmethod
    def delete_file(
        cookie_manager: CookieManager, file_name: str, document_ids: list[str], session_id: str | None = None
    ) -> bool:
        if not cookie_manager.ready():
            st.stop()
        try:
            session_id_entry = {"sessionId": session_id} if session_id else {}
            response = requests.delete(
                f"{backend_url}/delete_file",
                data={
                    "filename": file_name,
                    "documentIds": json.dumps(document_ids),
                    **session_id_entry,
                },
            )
            json_response = response.json()
            if json_response["error"] != "":
                raise Exception(json_response["error"])
            response_message = json_response["message"]
            st.toast(response_message, icon="✅")
            return True
        except Exception as err:
            st.error(err, icon="❌")
        return False

    @staticmethod
    def prompt(cookie_manager: CookieManager, text_prompt: str, session_id: str | None = None) -> Result | None:
        if not cookie_manager.ready():
            st.stop()
        try:
            session_id_dict = {"sessionId": session_id} if session_id is not None else {}
            response = requests.post(f"{backend_url}/prompt", data={"prompt": text_prompt, **session_id_dict})
            json_response = response.json()
            if json_response["error"] != "":
                st.error(json_response["error"], icon="❌")
                return None
            result = json_response["result"]
            citations = result["citations"]["citations"]
            source_docs = result["source_documents"]
            answer = result["answer"]
            return answer, citations, source_docs
        except Exception as err:
            st.error(err)

    @staticmethod
    def clear_chat_history(cookie_manager: CookieManager, session_id: str | None = None) -> bool:
        if not cookie_manager.ready():
            st.stop()
        try:
            session_id_entry = {"sessionId": session_id} if session_id else {}
            response = requests.delete(f"{backend_url}/clear_chat_history", data={**session_id_entry})
            json_response = response.json()
            if json_response["error"] != "":
                raise Exception(json_response["error"])
            response_message = json_response["message"]
            st.toast(response_message, icon="✅")
            return True
        except Exception as err:
            st.error(err, icon="❌")
        return False
    
    @staticmethod
    def send_final_answer(final_answer: BotMessage, cookie_manager: CookieManager, session_id: str | None = None) -> bool:
        if not cookie_manager.ready():
            st.stop()
        try:
            session_id_entry = {"sessionId": session_id} if session_id else {}
            response = requests.post(f"{backend_url}/submit_final_answer", data={**session_id_entry}, json=final_answer)
            json_response = response.json()
            if json_response["error"] != "":
                raise Exception(json_response["error"])
            response_message = json_response["message"]
            st.toast(response_message, icon="✅")
            return True
        except Exception as err:
            st.error(err, icon="❌")
        return False

        
