import streamlit as st
import google.generativeai as genai
import datetime

# PASTIIN API KEY BARU KAMU SUDAH DI SINI
API_KEY = "AIzaSyDwU3k_Q1ZMUeeGMn3GYf7PE16n41cIDjw"
genai.configure(api_key=API_KEY)

# FUNGSI ANTI-404: Mencoba semua kemungkinan nama model
def panggil_model():
    # Daftar variasi nama model yang sering dikenali server berbeda
    variasi_nama = ['gemini-pro', 'models/gemini-pro', 'gemini-1.5-flash', 'models/gemini-1.5-flash']
    for nama in variasi_nama:
        try:
            m = genai.GenerativeModel(nama)
            # Tes panggil singkat untuk pastikan modelnya ada
            m.generate_content("test") 
            return m
        except:
            continue
    return None

model = panggil_model()

st.set_page_config(page_title="NIMANG Studio", page_icon="🌚")

st.title("🌚 NIMANG")
st.caption(f"WOLATANG BERSEJARAH | {datetime.date.today().strftime('%d %B %Y')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya koding, makalah, atau tugas UNTRIB..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None:
            st.error("Gagal terhubung ke AI. Silakan cek API Key dan tekan REBOOT di dashboard Streamlit.")
        else:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Eror sistem: {str(e)}")
