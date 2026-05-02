import streamlit as st
import pandas as pd
import requests
import sympy as sp

st.set_page_config(page_title="Alor.GPT", layout="centered")

# CSS Minimalis & Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, div { color: white !important; font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.markdown("<h2 style='text-align: center; margin-top: 100px;'>Ready when you are.</h2>", unsafe_allow_html=True)
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya apa saja..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # 1. CEK DATA MAHASISWA UNTRIB (Prioritas Lokal)
        try:
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil_mhs = df[df.apply(lambda row: prompt.lower() in row.astype(str).str.lower().values, axis=1)]
            if not hasil_mhs.empty:
                answer = f"📋 **Data Mahasiswa UNTRIB:**\n\n{hasil_mhs.to_markdown()}"
                response_placeholder.markdown(answer)
            else:
                raise Exception("Bukan data mahasiswa")
        except:
            # 2. PROSES SEMUA PERTANYAAN (Matematika & Umum) SECARA KILAT
            # Menggunakan Wikipedia/DuckDuckGo API untuk jawaban instan
            try:
                url = f"https://api.duckduckgo.com/?q={prompt}&format=json&no_html=1&skip_disambig=1"
                data = requests.get(url).json()
                
                if data.get("Abstract"):
                    answer = data["Abstract"]
                    if data.get("Image"):
                        st.image(f"https://duckduckgo.com{data['Image']}", width=250)
                elif data.get("Answer"): # Untuk soal matematika/konversi cepat
                    answer = f"💡 **Jawaban Instan:** {data['Answer']}"
                else:
                    # Jika buntu, gunakan logika matematika internal
                    try:
                        p_math = prompt.lower().replace('akar', 'sqrt').replace('bagi', '/').replace('kali', '*')
                        res = sp.sympify(p_math)
                        answer = f"🔢 **Hasil Hitung:** {res.evalf() if res.is_number else res}"
                    except:
                        answer = f"Saya mengerti pertanyaan Anda tentang '{prompt}'. Namun, saya butuh informasi lebih spesifik untuk menjawabnya dengan tepat."
                
                response_placeholder.markdown(answer)
            except:
                answer = "Koneksi terputus, coba lagi sebentar."
                response_placeholder.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
