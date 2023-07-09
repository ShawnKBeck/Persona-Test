import os
import openai
import streamlit as st
from streamlit.server.server import Server

openai.api_key = st.secrets["OPENAI_API_KEY"]

system_prompt = """..."""  # Include the full system prompt here

# The 'system' message to set up the assistant's behavior
system_message = {"role": "system", "content": system_prompt}

def get_state():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Could not get Streamlit session.")
    return session_info.session._main_dg._get_state()

def ask_gpt3(question, messages):
    user_message = {"role": "user", "content": question}
    messages.append(user_message)
    response = openai.ChatCompletion.create(
        model="gpt-4-0314",
        messages=messages
    )
    return response.choices[0].message['content']

st.title('Shawn Beck')

state = get_state()

if 'messages' not in state:
    state['messages'] = [system_message]

question = st.text_input("I am Shawn Beck. Ask my anything:")
if st.button('Ask'):
    response = ask_gpt3(question, state['messages'])
    state['messages'].append({"role": "assistant", "content": response})
    st.write(response)
