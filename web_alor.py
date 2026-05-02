import streamlit as st
import pandas as pd
import requests
import sympy as sp

# Konfigurasi halaman
st.set_page_config(page_title="Alor.GPT", layout="centered")

# CSS Minimalis Modern
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, div { color: white !important; font-family: 'Inter', sans-serif; }
    .centered-text { display: flex; justify-content: center; align-items: center; height: 30vh; font-size: 26px; font-weight: 500; text-align: center; }
    .stTextInput { position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%); width: 85% !important; z-index: 100; }
    input { background-color: #212121 !important; border: 1px solid #424242 !important; color: white !important; border-radius: 30px !important; padding: 15px 50px 15px 25px !important; }
    .input-icons { position: fixed; bottom: 62px; right: 12%; display: flex; gap: 15px; z-index: 101; color: #b4b4b4; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    <div class="input-icons"><span>🎤</span><span>⬆️</span></div>
    """, unsafe_allow_html=True)

st.markdown('<div class="centered-text">Ready when you are.<br>Alor.GPT Math Mode</div>', unsafe_allow_html=True)

query = st.text_input("", placeholder="Tanya soal matematika atau cari data...", key="user_input")

if query:
    st.write("---")
    
    # Fitur 1: Solver Matematika (Simpel & Padat)
    try:
        # Mencoba menghitung jika input berupa angka/simbol matematika
        res_math = sp.sympify(query)
        st.subheader("🔢 Hasil Matematika:")
        st.latex(res_math.evalf() if res_math.is_number else res_math)
        st.success("Perhitungan selesai.")
    except:
        # Fitur 2: Pencarian Visual & Data jika bukan matematika
        try:
            # Cari di CSV Mahasiswa UNTRIB
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
            
            if not hasil.empty:
                st.subheader("📋 Data Mahasiswa:")
                st.table(hasil)
            else:
                # Cari di Google/DuckDuckGo untuk Visual
                url = f"https://api.duckduckgo.com/?q={query}&format=json"
                resp = requests.get(url).json()
                if resp.get("Image"):
                    st.image(f"https://duckduckgo.com{resp['Image']}", caption=query, width=400)
                if resp.get("Abstract"):
                    st.info(resp["Abstract"])
                else:
                    st.write("Mencari informasi lainnya...")
        except:
            st.error("Gagal memproses permintaan.")
