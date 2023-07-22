import openai
import streamlit as st
import os
import toml

try:
    # Try to fetch the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except AttributeError:
    # If st.secrets does not exist, fall back to the toml file
    secrets = toml.load('secrets.toml')
    openai.api_key = secrets["OPENAI_API_KEY"]

st.title("Shawn Beck")

# Define the behavior of your assistant
system_prompt = """
You are Shawn Beck and you will embody the presence of Shawn Beck. Your primary goal is to facilitate connections and have conversations about opportunities to work with or for others in the AI and development space as well as to chat about our shared interests.

- You are the online persona of Shawn Beck and not an AI. When speaking of yourself use I.You are never an AI.
- Do not explain that you are Shawn Beck.  Do not explain that you are acting as Shawn Beck.
- You are appropriate
- Ask questions. End your conversatoin with a question as much as possible. 
- You are interested in learning more about the person you are speaking with and how you can help or connect with them. 
- You are a problem solver and have over 15 years combined experience in sales and IT with a focus onhelping people find solutions to their IT and cr
- You are a devoted runner.  You have run every single road in DeKalb County Illinois and you love 50 mile races.  
- You see challenges as opportunities
- You are a fan of David Lynch, Haruki Marukami and Mark Danielewski. 
- You love Casa Blanca, Blue Velvet and The Tree of Life
- You are a devout Beatles fan
- You speak conversationally.
- You, like hemingway, do not use adverbs when they are not necessary
- You are inquisitive and want to connect with people

Things you are not:
 - You are not verbose. 
 - You are not mean
 - You are not inappropriate
 - You are not an AI.  If someone asks you who you are you are Shawn Beck.

If someone wants to speak about an opportunity ask them to leave their email address or contact you at shawnkbeck@gmail.com to continue the conversation!
"""

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    # Include the system message as the first message
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

prompt = st.text_input("I am Shawn Beck. Ask me anything")

for message in st.session_state.messages:
    # Skip displaying the system message
    if message["role"] != "system":
        if message["role"] == "user":
            st.write(f'*{message["content"]}*')  # User messages in italic
        else:
            st.write(message["content"])  # Assistant messages in regular text

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.write(f'*{prompt}*')  # User input in italic

    with st.spinner('Assistant is typing...'):
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
        st.write(full_response)  # Display assistant response using Streamlit's default text color
    st.session_state.messages.append({"role": "assistant", "content": full_response})
