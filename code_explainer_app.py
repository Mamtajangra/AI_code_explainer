# os: helps  Python app interact with  computer’s environment (for reading API keys, etc.).
# dotenv: used to load hidden or secret information (like API keys) from a .env file.
# streamlit: builds the interactive web app interface.
# openai: is a library used here to talk to the Groq API, because Groq’s API follows the OpenAI-compatible format.'''

import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

#  Load environment variables
# store api key in groq_key

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

#  Configure the client (Groq uses OpenAI-compatible API)
# This creates a client object that talks to Groq’s server.
# base_url → tells Python, “Hey, connect to Groq’s API, not OpenAI’s.”
# api_key=groq_key → authenticates you (like a password for Groq’s system).

client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=groq_key)

#  Choose a Groq-supported model
MODEL =  "openai/gpt-oss-20b" 

# Streamlit UI
# st.set_page_config(page_title="AI Code Explainer")
# st.title() → shows a big heading on your app page.
# st.write() → displays a small paragraph under the title.

st.title(" AI Code Explainer (Groq Powered)")
st.write("Paste your code below and get a clear explanation powered by Groq API!")

#  Input box
# Creates a text box for users to paste their code.
# height=200 → makes the box tall enough.
# placeholder → shows a light hint text when the box is empty.

code_input = st.text_area("Enter your code here:", height=200, placeholder="Paste Python, C++, or JS code...")

#  Button click event
if st.button("Explain Code"):
    # .strip() removes spaces or blank lines.
    #  This condition checks: “Did the user actually paste something?”
    # If yes → it goes ahead and explains.
    # If no → it shows a warning message.
    if code_input.strip():
        # This displays a “loading” animation with a message — while Groq is thinking.
        with st.spinner("Analyzing your code using Groq..."):

            # Builds the instruction for the AI model.
            # It tells Groq: “Please explain this code line by line.”
            # {code_input} dynamically inserts the user’s pasted code into the prompt.
            prompt = f"Explain the following code line by line in simple and easy-to-understand language:\n\n{code_input}"
            
            # model=MODEL	Which AI brain to use
            # messages=	A conversation list between "system" and "user"
            # role: system	Tells the AI how to behave (like a teacher)
            # role: user	The user’s actual question or request
            # temperature=0.3	Controls creativity — smaller means more accurate and less random
            # this line sends the request → AI processes it → sends the explanation back.
            response = client.chat.completions.create(model=MODEL,
                messages=[{"role": "system", "content": "You are an expert code explainer."},
                    {"role": "user", "content": prompt}],temperature=0.3,)
# The model’s reply is stored inside a big JSON structure.
# This line extracts the actual text explanation from that structure.
            explanation = response.choices[0].message.content

# Displays a heading “Code Explanation”.
        st.markdown("###  Code Explanation:")
        st.write(explanation)

        # If user clicks button but doesn’t paste any code — this message pops up.
    else:
        st.warning(" Please paste some code before explaining!")
