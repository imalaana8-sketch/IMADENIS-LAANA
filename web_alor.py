import streamlit as st
import google.generativeai as genai

# TEMPELKAN API KEY BARU DI SINI
API_KEY = "AIzaSyDqCqGvdtM80fiVkvNuMcg2TBq3EeqmCBA" 
genai.configure(api_key=API_KEY)

st.title("🌚 NIMANG")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya apa saja..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Pakai model paling stabil sejagat AI
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Eror: {str(e)}")
