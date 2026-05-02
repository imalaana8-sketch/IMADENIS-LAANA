import streamlit as st
import pandas as pd
import google.generativeai as genai

# Inisialisasi API
API_KEY = "AIzaSyDkTBGovE1LriT4e21ia2EhPa1DLLOq0Ho"
genai.configure(api_key=API_KEY)

# Mencoba menggunakan model yang paling tersedia (Flash Terbaru)
try:
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Alor.GPT - Super AI", layout="centered")

st.markdown("<style>.stApp { background-color: #0d0d0d; } h1, h2, h3, p, span, div { color: #ececec !important; font-family: 'Inter', sans-serif; } #MainMenu, footer, header {visibility: hidden;}</style>", unsafe_allow_html=True)

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
        full_response = ""
        # Prioritas 1: Data Mahasiswa UNTRIB
        try:
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
            if not hasil.empty:
                full_response = f"📋 **Data Mahasiswa UNTRIB:**\n\n{hasil.to_markdown()}"
        except:
            pass

        # Prioritas 2: Otak AI Gemini
        if not full_response:
            try:
                response = model.generate_content(prompt)
                full_response = response.text
            except Exception as e:
                full_response = f"Sistem sedang sibuk, coba ulangi: {str(e)}"

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
