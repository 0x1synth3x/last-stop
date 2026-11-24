# I def didnt create it 3am
# I dont know if this will work cuz i am learning streamlit by doing

import streamlit as st
import random
import time

st.set_page_config(page_title="ghostTTY", page_icon="💀", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; }
    .terminal-box {
        font-family: 'Courier New', monospace;
        background-color: #111;
        border: 1px solid #333;
        border-radius: 4px;
        padding: 20px;
        color: #0f0;
        min-height: 400px;
        white-space: pre-wrap;
        font-size: 14px;
    }
    .red-text { color: #f00; font-family: 'Courier New', monospace; }
    .dim-text { color: #555; font-family: 'Courier New', monospace; }
    .yellow-text { color: #ff0; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# streamlit reruns everything so i need this
if "history" not in st.session_state:
    st.session_state.history = []
if "here" not in st.session_state:
    st.session_state.here = "home/user"
if "wound" not in st.session_state:
    st.session_state.wound = 0
if "read" not in st.session_state:
    st.session_state.read = set()

if len(st.session_state.history) == 0:
    st.session_state.history = [
        "<span class='yellow-text'>g h o s t T T Y  v0.6.6.6</span>",
        "",
        "hello.",
        "friend.",
        "",
        "<span class='yellow-text'>Last login: Tue Nov 24 03:00:01 2026 on tty1</span>",
        "<span class='yellow-text'>Welcome to machine. You have mail.</span>",
        "",
        "a note is pinned to your screen:",
        "",
        "<b>'check the system logs. something's wrong.'</b>",
        "",
        "<span class='dim-text'>type 'help' if you need it. you won't.</span>",
        "",
    ]

# show the terminal
display = st.session_state.history[-30:]
st.markdown(f"<div class='terminal-box'>{'<br>'.join(display)}</div>", unsafe_allow_html=True)

# taking input
user_input = st.text_input("", placeholder="guest@machine:~$ ", label_visibility="collapsed")

if st.button("⏎") and user_input:
    user_input = user_input.strip()
    st.session_state.history.append(f"guest@machine:~$ {user_input}")

    # for now just echo back
    st.session_state.history.append(f"bash: {user_input}: command not found")
    st.rerun()

st.markdown("<span class='dim-text' style='font-family:monospace;font-size:11px;'>ghostTTY v0.6.6.6</span>", unsafe_allow_html=True)