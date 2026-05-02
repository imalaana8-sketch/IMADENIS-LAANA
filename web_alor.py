import streamlit as st
import google.generativeai as genai
from PIL import Image

# Pastikan API KEY terbaru kamu sudah di sini
API_KEY = "AIzaSyC7tir9Es8qIrYbq2BHNmgDdmQmeV05Xc4"
genai.configure(api_key=API_KEY)

# Fungsi untuk memilih model yang tersedia secara otomatis
def muat_model():
    # Daftar model dari yang terbaru ke yang paling stabil
    daftar_model = ['models/gemini-pro']
    for nama in daftar_model:
        try:
            model_uji = genai.GenerativeModel(nama)
            # Tes panggil model
            return model_uji
        except:
            continue
    return None

model = muat_model()

st.set_page_config(page_title="NIMANG - Wolatang Bersejarah", layout="centered")

# Tampilan Header sesuai screenshot kamu
st.title("🌚 NIMANG")
st.caption("WOLATANG BERSEJARAH | 02 May 2026")

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
        if model is None:
            st.error("Gagal memuat model AI. Periksa kembali API Key atau koneksi server.")
        else:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Kendala Studio: {str(e)}")
