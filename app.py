import streamlit as st
from ragpycharm import get_answer_from_pdf

st.title("Şevval's ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("🌸 🌺 🌷 Buraya yazabilirsin... 🌷 🌺 🌸"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            answer = get_answer_from_pdf(prompt)

            st.balloons()

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"An error occurred: {e}")

