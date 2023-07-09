import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

system_prompt = """..."""  # Include the full system prompt here

# The 'system' message to set up the assistant's behavior
system_message = {"role": "system", "content": system_prompt}

def ask_gpt3(question, messages):
    user_message = {"role": "user", "content": question}
    messages.append(user_message)
    response = openai.ChatCompletion.create(
        model="gpt-4-0314",
        messages=messages
    )
    return response.choices[0].message['content']

st.title('Shawn Beck')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [system_message]

question = st.text_input("I am Shawn Beck. Ask my anything:")
if st.button('Ask'):
    response = ask_gpt3(question, st.session_state['messages'])
    st.session_state['messages'].append({"role": "assistant", "content": response})
    st.write(response)

