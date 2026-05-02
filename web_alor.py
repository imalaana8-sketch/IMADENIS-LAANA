import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import datetime

# 1. KONFIGURASI API
API_KEY = "AIzaSyDmB0zKl1df5Dvv46ENH2RMpg3LKU8qi3U"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Alor.GPT Pro Max", layout="wide")

# 2. TAMPILAN INTERFACE (CSS EKSKLUSIF)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stChatInput { bottom: 20px; }
    .report-box { 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #238636; 
        background-color: #161b22;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MANAJEMEN RIWAYAT & DRAFT
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR: UNTUK UNGGAH DOKUMEN & RIWAYAT
with st.sidebar:
    st.title("📂 Dokumen & Arsip")
    
    # Fitur Unggah Semua Jenis Dokumen
    st.subheader("📤 Unggah File (All Formats)")
    uploaded_file = st.file_uploader(
        "Pilih Foto, PDF, Word, Excel, atau PPT", 
        type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx', 'pptx', 'txt']
    )
    
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' berhasil dimuat!")
        st.info("AI sekarang bisa membaca isi dokumen ini untuk ringkasan atau makalah.")

    st.divider()
    st.subheader("📜 Riwayat Pencarian")
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.caption(f"{i+1}. {msg['content'][:30]}...")

# 4. TAMPILAN UTAMA
st.title("🤖 Alor.GPT Pro Max")
st.write(f"📅 Tanggal Hari Ini: {datetime.date.today().strftime('%d %B %Y')}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIKA PEMROSESAN MAKALAH & RINGKASAN
if prompt := st.chat_input("Contoh: 'Buatkan makalah tentang IT' atau 'Ringkas file ini'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Instruksi Khusus Makalah & Ringkasan Eksklusif
        now = datetime.datetime.now()
        context = f"""
        Kamu adalah Alor.GPT Pro Max. 
        Tugas khusus:
        1. Jika diminta membuat MAKALAH: Gunakan struktur (Kata Pengantar, Bab 1 Pendahuluan, Bab 2 Pembahasan, Bab 3 Penutup). 
           Wajib sertakan Daftar Pustaka dengan alamat URL, tahun {now.year}, dan catatan kaki (footnote).
        2. Jika ada file PPT/Excel/Doc: Berikan ringkasan eksklusif dalam format tabel atau list yang sangat rapi.
        3. Gunakan bahasa Indonesia yang formal namun cerdas.
        4. Referensi harus otomatis mencantumkan tanggal akses hari ini: {now.strftime('%d-%m-%Y')}.
        """

        try:
            # Gabungkan input dengan file jika ada
            if uploaded_file:
                # Mengirimkan informasi nama file ke AI sebagai konteks
                user_input = f"User mengunggah file: {uploaded_file.name}. Instruksi: {prompt}"
                response = model.generate_content([context, user_input])
            else:
                response = model.generate_content(context + prompt)
            
            full_response = response.text
            
            # Tampilkan dalam kotak eksklusif jika ini ringkasan/makalah
            if "Bab 1" in full_response or "Ringkasan" in full_response:
                st.markdown(f'<div class="report-box">{full_response}</div>', unsafe_allow_html=True)
            else:
                st.markdown(full_response)
                
        except Exception as e:
            full_response = f"⚠️ Maaf, sistem sedang memproses file besar. Eror: {str(e)}"
            st.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
