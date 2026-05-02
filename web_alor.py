import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# 1. Inisialisasi API - Pastikan API Key ini benar
API_KEY = "AIzaSyDmB0zKl1df5Dvv46ENH2RMpg3LKU8qi3U"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Alor.GPT Pro - Visual & Text", layout="centered")

# Desain Tampilan
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; }
    h1, h2, h3, p, span, div { color: #ececec !important; }
    .stChatInput { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Alor.GPT Pro")
st.caption("Sekarang bisa baca Foto, File Teks, dan Edit Gambar")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FITUR UNGGAH FILE (Galeri/Dokumen) ---
with st.sidebar:
    st.header("📁 Unggah File")
    uploaded_file = st.file_uploader("Pilih Foto atau Dokumen", type=['png', 'jpg', 'jpeg', 'txt', 'csv'])
    
    if uploaded_file is not None:
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            img = Image.open(uploaded_file)
            st.image(img, caption="Foto Berhasil Dimuat", use_container_width=True)
            st.success("Foto siap dianalisis/diedit!")
        else:
            st.info("File teks/dokumen berhasil dimuat.")

# Tampilkan Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- SISTEM PROSES (Teks & Foto) ---
if prompt := st.chat_input("Tanya atau beri instruksi edit foto..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = ""
        
        try:
            if uploaded_file is not None and uploaded_file.type in ["image/png", "image/jpeg"]:
                # Jika ada foto, AI akan menganalisis foto tersebut berdasarkan instruksi kamu
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
                full_response = response.text
            else:
                # Jika hanya teks atau cek data mahasiswa UNTRIB
                try:
                    df = pd.read_csv("mahasiswa_untrib.csv")
                    hasil = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
                    if not hasil.empty:
                        full_response = f"📋 **Data Mahasiswa UNTRIB:**\n\n{hasil.to_markdown()}"
                except:
                    pass
                
                if not full_response:
                    response = model.generate_content(prompt)
                    full_response = response.text
        except Exception as e:
            full_response = f"Waduh, ada kendala: {str(e)}"

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
