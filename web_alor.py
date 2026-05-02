import streamlit as st
import pandas as pd
import requests
import sympy as sp

# Konfigurasi halaman
st.set_page_config(page_title="Alor.GPT", layout="centered")

# CSS untuk tampilan Dark Mode Total & Minimalis
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, div { color: white !important; font-family: 'Inter', sans-serif; }
    .stChatFloatingInputContainer { background-color: transparent !important; }
    .stChatMessage { background-color: #1a1a1a !important; border-radius: 15px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Judul Utama di Tengah
if "messages" not in st.session_state:
    st.markdown("<h2 style='text-align: center; margin-top: 150px;'>Ready when you are.</h2>", unsafe_allow_html=True)
    st.session_state.messages = []

# Menampilkan riwayat chat agar jawaban tidak hilang
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# FITUR UTAMA: Tombol Kirim Otomatis (st.chat_input)
# Catatan: Untuk Mic, browser HP biasanya sudah menyediakan ikon mic di keyboard Android kamu
if prompt := st.chat_input("Ask anything..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses Jawaban Kilat
    with st.chat_message("assistant"):
        response_container = st.empty()
        
        # 1. Cek Matematika (Sangat Cepat)
        try:
            # Membersihkan input dari simbol aneh seperti 'x' menjadi '*'
            clean_prompt = prompt.replace('×', '*').replace(':', '/')
            res_math = sp.sympify(clean_prompt)
            answer = f"🔢 **Hasil:** {res_math.evalf() if res_math.is_number else res_math}"
        except:
            # 2. Cek Data Mahasiswa UNTRIB
            try:
                df = pd.read_csv("mahasiswa_untrib.csv")
                hasil = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
                if not hasil.empty:
                    answer = f"📋 **Data Ditemukan:**\n\n{hasil.to_markdown()}"
                else:
                    # 3. Pencarian Visual Google/DuckDuckGo
                    url = f"https://api.duckduckgo.com/?q={prompt}&format=json"
                    resp = requests.get(url).json()
                    if resp.get("Abstract"):
                        answer = resp["Abstract"]
                        if resp.get("Image"):
                            st.image(f"https://duckduckgo.com{resp['Image']}", width=300)
                    else:
                        answer = "Maaf, saya tidak menemukan informasi spesifik. Coba gunakan kata kunci lain."
            except:
                answer = "Sistem sedang sibuk, coba lagi nanti."

        response_container.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
