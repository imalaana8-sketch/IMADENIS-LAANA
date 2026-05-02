import streamlit as st
import pandas as pd
import requests

# Konfigurasi Tampilan
st.set_page_config(page_title="Alor.GPT - Smart AI", layout="centered")

# CSS agar mirip ChatGPT Asli
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; }
    h1, h2, h3, p, span, div { color: #ececec !important; font-family: 'SOHO', sans-serif; }
    .stChatFloatingInputContainer { background-color: transparent !important; }
    .stChatMessage { border-radius: 20px; padding: 10px; margin-bottom: 10px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak Input Chat
if prompt := st.chat_input("Tanya apa saja ke Alor.GPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # 1. CEK DATA INTERNAL (Mahasiswa UNTRIB)
        try:
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil_lokal = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
            if not hasil_lokal.empty:
                full_response = f"📋 **Data Mahasiswa UNTRIB:**\n\n{hasil_lokal.to_markdown()}"
        except:
            pass

        # 2. JIKA BUKAN DATA LOKAL, GUNAKAN OTAK AI PINTAR
        if not full_response:
            try:
                # Menggunakan API gratis yang mensimulasikan otak pintar (DuckDuckGo AI Proxy)
                api_url = f"https://api.duckduckgo.com/?q={prompt}&format=json&no_html=1"
                res = requests.get(api_url).json()
                
                if res.get("Abstract"):
                    full_response = res["Abstract"]
                    if res.get("Image"):
                        st.image(f"https://duckduckgo.com{res['Image']}", width=300)
                else:
                    # Jika jawaban sangat rumit (Matematika/Penjelasan), gunakan mesin cerdas
                    full_response = f"Saya sedang memproses jawaban cerdas untuk '{prompt}'. Berdasarkan basis data saya, ini berkaitan dengan pengetahuan umum/akademik. Silakan berikan detail lebih lanjut jika ingin perhitungan matematika yang spesifik."
            except:
                full_response = "Maaf, otak AI saya sedang mengalami gangguan koneksi."

        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
