import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import datetime

# 1. KONFIGURASI API
API_KEY = "AIzaSyDmB0zKl1df5Dvv46ENH2RMpg3LKU8qi3U"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Alor.GPT Pro Max - Studio Kreatif", layout="wide")

# 2. TAMPILAN INTERFACE (STYLE STUDIO)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .report-box { padding: 20px; border-radius: 10px; border: 1px solid #30363d; background-color: #161b22; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #238636; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: TOOLS KREATIF & DOKUMEN
with st.sidebar:
    st.title("🎨 Alor Studio")
    
    # Fitur Unggah Multi-Fungsi
    uploaded_file = st.file_uploader(
        "Unggah Foto atau Dokumen", 
        type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx', 'pptx']
    )
    
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' siap diproses!")
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(Image.open(uploaded_file), caption="Preview Foto")

    st.divider()
    st.subheader("🛠️ Fitur Edit Otomatis")
    mode_edit = st.selectbox("Pilih Aksi Kreatif:", [
        "Analisis Teks & Dokumen",
        "Ubah Foto ke Anime/Kartun",
        "Perbaiki Foto Buram (Enhance)",
        "Ganti Background Foto",
        "Ubah Foto Jadi Video Gerak",
        "Video + Suara (Text-to-Speech)"
    ])

# 4. TAMPILAN UTAMA
st.title("🤖 Alor.GPT Studio")
st.caption(f"Aktif di Universitas Tribuana Kalabahi | {datetime.date.today().strftime('%d %B %Y')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIKA PEMROSESAN SUPER AI
if prompt := st.chat_input("Berikan instruksi (contoh: 'Ganti background ke pantai' atau 'Buat makalah')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = ""
        
        # Konteks Khusus Studio Kreatif
        context = f"""
        Kamu adalah Alor.GPT Studio Kreatif. 
        Tugas:
        1. Mode Anime/Video: Jelaskan cara AI memproses transformasi visual dari foto ke anime.
        2. Mode Enhance: Berikan instruksi teknis untuk menajamkan bagian foto yang buram.
        3. Background: Simulasikan perubahan latar belakang sesuai permintaan user.
        4. Text-to-Video: Buatkan naskah dan deskripsi gerakan video beserta narasi suara yang sesuai ketikan user.
        5. Akademik: Tetap sediakan fitur Makalah Bab 1-3 lengkap dengan sumber dan catatan kaki.
        """

        try:
            if uploaded_file:
                # Memproses Foto/Dokumen dengan instruksi edit
                response = model.generate_content([f"MODE: {mode_edit}. INSTRUKSI: {prompt}. CONTEXT: {context}", Image.open(uploaded_file) if "image" in uploaded_file.type else uploaded_file.name])
            else:
                response = model.generate_content(context + prompt)
            
            full_response = response.text
            
            # Tampilan hasil eksklusif
            if "Video" in mode_edit or "Anime" in mode_edit:
                st.info(f"✨ Memproses Mode: {mode_edit}...")
                st.markdown(f'<div class="report-box"><b>Hasil Studio:</b><br>{full_response}</div>', unsafe_allow_html=True)
            else:
                st.markdown(full_response)
                
        except Exception as e:
            full_response = f"⚠️ Kendala Studio: {str(e)}"
            st.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
