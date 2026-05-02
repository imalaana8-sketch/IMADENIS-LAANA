import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime

# 1. KONFIGURASI API (Gunakan API Key terbaru kamu)
API_KEY = "GANTI_DENGAN_API_KEY_BARU_KAMU"
genai.configure(api_key=API_KEY)

# 2. PENGATURAN MINICON (FAVICON) & PAGE
# '🤖' adalah ikon umum yang akan muncul di tab browser (favicon)
st.set_page_config(
    page_title="NIMANG Studio", 
    page_icon="🤖", 
    layout="centered"
)

# 3. FUNGSI OTOMATISASI MODEL
def muat_model_otomatis():
    # Mencoba model terbaru, jika gagal pindah ke model stabil secara otomatis
    untuk_dicoba = ['gemini-1.5-flash', 'gemini-pro']
    for nama in untuk_dicoba:
        try:
            return genai.GenerativeModel(nama)
        except:
            continue
    return None

model = muat_model_otomatis()

# 4. TAMPILAN INTERFACE (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    code { color: #ff79c6 !important; background-color: #282a36; padding: 2px 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌚 NIMANG")
st.caption(f"WOLATANG BERSEJARAH | {datetime.date.today().strftime('%d %B %Y')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIKA OTOMATISASI PEMROGRAMAN & DOKUMEN
if prompt := st.chat_input("Tanya koding, makalah, atau tugas UNTRIB..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None:
            st.error("Sistem sedang sinkronisasi. Silakan refresh halaman.")
        else:
            try:
                # Instruksi agar AI otomatis mendeteksi bahasa pemrograman dan format akademik
                konteks = """
                Kamu adalah NIMANG AI. 
                1. Jika user bertanya tentang koding, tampilkan kode secara otomatis dalam blok kode yang rapi.
                2. Jika user meminta makalah, buatkan Bab 1-3 dengan referensi otomatis.
                3. Gunakan gaya bahasa profesional untuk mahasiswa Universitas Tribuana Kalabahi.
                """
                response = model.generate_content(konteks + prompt)
                full_response = response.text
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {str(e)}")
