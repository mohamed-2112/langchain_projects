from pathlib import Path
from typing import Set

from dotenv import load_dotenv

from backend.core import DocHelper
import streamlit as st
from streamlit_chat import message

env_path = "D:\pythonProjects\langchain_courses\langchain_projects\config\.env"
load_dotenv(dotenv_path=env_path)

st.header("langChain udemy course- documentation helper bot")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here....")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def create_source_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources: \n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        docHelper_backend = DocHelper()
        generated_response = docHelper_backend.run(query=prompt, chat_history=st.session_state["chat_history"])
        sources = set([doc.metadata["source"] for doc in generated_response["source_documents"]])
        formatted_response = f"{generated_response['answer']} \n\n {create_source_string(sources)}"

        st.session_state['user_prompt_history'].append(prompt)
        st.session_state['chat_answers_history'].append(formatted_response)
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    for response, user_query in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
        message(user_query, is_user=True)
        message(response)
