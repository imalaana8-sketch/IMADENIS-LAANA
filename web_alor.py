import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import time

# 1. KONFIGURASI API
API_KEY = "AIzaSyDmB0zKl1df5Dvv46ENH2RMpg3LKU8qi3U"
genai.configure(api_key=API_KEY)
# Menggunakan Gemini 1.5 Flash untuk kecepatan dan fitur foto/coding
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Alor.GPT Pro + History", layout="wide")

# 2. TAMPILAN INTERFACE (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ececec; }
    .stChatInput { bottom: 20px; }
    .sidebar-text { font-size: 14px; color: #bbbbbb; }
    code { color: #ff79c6 !important; } /* Warna untuk kode pemrograman */
    </style>
    """, unsafe_allow_html=True)

# 3. MANAJEMEN RIWAYAT (HISTORY/DRAFT)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar untuk Fitur Tambahan
with st.sidebar:
    st.title("📂 Menu Alor.GPT")
    
    # Fitur Unggah Foto/Galeri
    st.subheader("🖼️ Media & Dokumen")
    uploaded_file = st.file_uploader("Unggah Foto/File Teks", type=['png', 'jpg', 'jpeg', 'txt'])
    if uploaded_file and uploaded_file.type in ["image/png", "image/jpeg"]:
        st.image(Image.open(uploaded_file), caption="Preview Foto", use_container_width=True)

    st.divider()
    
    # Riwayat Pencarian (Draft)
    st.subheader("📜 Riwayat Chat")
    if st.button("🗑️ Hapus Semua Riwayat"):
        st.session_state.messages = []
        st.rerun()
    
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.write(f"{i+1}. {msg['content'][:25]}...")

# 4. TAMPILAN UTAMA
st.title("🤖 Alor.GPT Pro")
st.caption("Mendukung: Pemrograman, Foto, Alkitab, & Lagu Pujian")

# Menampilkan Riwayat di Layar Utama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIKA PEMROSESAN (AI)
if prompt := st.chat_input("Tanya coding, ayat Alkitab, atau analisis foto..."):
    # Simpan input ke riwayat agar tidak terhapus
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Pesan instruksi khusus untuk AI
        context = """
        Kamu adalah Alor.GPT Pro. Kamu ahli dalam:
        1. Bahasa Pemrograman (Python, PHP, HTML, CSS, Javascript, dll).
        2. Menjelaskan ayat-ayat Alkitab dan memberikan Lagu Pujian Kristen.
        3. Menganalisis foto yang diunggah pengguna.
        4. Membantu mahasiswa Universitas Tribuana Kalabahi (UNTRIB).
        Jawablah dengan sopan dan detail.
        """

        try:
            # Jika ada file yang diunggah
            if uploaded_file is not None and uploaded_file.type in ["image/png", "image/jpeg"]:
                img = Image.open(uploaded_file)
                response = model.generate_content([context + prompt, img])
                full_response = response.text
            else:
                # Cek data internal UNTRIB dulu
                try:
                    df = pd.read_csv("mahasiswa_untrib.csv")
                    hasil = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
                    if not hasil.empty:
                        full_response = f"📋 **Data Mahasiswa UNTRIB:**\n\n{hasil.to_markdown()}"
                except:
                    pass
                
                # Jika tidak ada di data lokal, tanya AI
                if not full_response:
                    response = model.generate_content(context + prompt)
                    full_response = response.text
        
        except Exception as e:
            full_response = f"⚠️ Ada kendala teknis: {str(e)}"

        response_placeholder.markdown(full_response)
        # Simpan jawaban ke riwayat (Draft)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
