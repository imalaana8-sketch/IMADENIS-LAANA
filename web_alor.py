import streamlit as st
import google.generativeai as genai
import datetime

# 1. TEMPELKAN KUNCI API BARU KAMU DI SINI
API_KEY = "AIzaSyDoitjL5tP9e45f1RROjdz4mnchIVgRreg"
genai.configure(api_key=API_KEY)

# 2. FUNGSI LISTMODELS OTOMATIS (Mencegah Error 404)
def dapatkan_model_tersedia():
    try:
        # Ini adalah cara memanggil list_models secara teknis
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Mengutamakan Flash, jika tidak ada pakai Pro
                if '1.5-flash' in m.name:
                    return genai.GenerativeModel(m.name)
        # Jika flash tidak ada dalam list, pakai yang paling standar
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        # Jika gagal list, pakai nama model standar sebagai cadangan terakhir
        return genai.GenerativeModel('models/gemini-pro')

model = dapatkan_model_tersedia()

st.set_page_config(page_title="NIMANG Studio", page_icon="🌚")

# Tampilan Header
st.title("🌚 NIMANG")
st.caption(f"WOLATANG BERSEJARAH | {datetime.date.today().strftime('%d %B %Y')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. PROSES INPUT
if prompt := st.chat_input("Tanya koding, makalah, atau tugas UNTRIB..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instruksi Otomatis agar AI pintar koding & makalah
            konteks = "Kamu adalah NIMANG AI. Bantu mahasiswa UNTRIB dengan koding rapi dan makalah lengkap."
            response = model.generate_content(konteks + prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ Kendala: {str(e)}")
            st.info("Saran: Pastikan API Key benar dan lakukan REBOOT di Dashboard Streamlit.")
