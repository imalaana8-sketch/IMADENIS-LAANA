import streamlit as st
import pandas as pd
import google.generativeai as genai

# KONFIGURASI: Ganti teks di bawah dengan kode AIzaSy... yang kamu copy tadi
API_KEY = "AIzaSyDmB0zKI1df5Dvv46ENH2RMpg3LKU8qi3U"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Alor.GPT - Super AI", layout="centered")

# CSS agar tampilan hitam elegan
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; }
    h1, h2, h3, p, span, div { color: #ececec !important; font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya apa saja ke Alor.GPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # 1. Cek Data Mahasiswa UNTRIB
        try:
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
            if not hasil.empty:
                full_response = f"📋 **Data Mahasiswa UNTRIB:**\n\n{hasil.to_markdown()}"
        except:
            pass

        # 2. Jika bukan data lokal, tanya Otak Gemini AI
        if not full_response:
            try:
                response = model.generate_content(prompt)
                full_response = response.text
            except:
                full_response = "Maaf, ada kendala pada koneksi otak AI saya."

        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
