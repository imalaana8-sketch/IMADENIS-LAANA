import streamlit as st
import pandas as pd
import requests

# Konfigurasi halaman agar berwarna gelap dan minimalis
st.set_page_config(page_title="Alor.GPT", layout="centered")

# CSS untuk membuat tampilan mirip ChatGPT (Latar belakang hitam, teks putih, input melayang)
st.markdown("""
    <style>
    .main {
        background-color: #000000;
    }
    .stApp {
        background-color: #000000;
    }
    h1, h2, h3, p, span, div {
        color: white !important;
        font-family: 'Inter', sans-serif;
    }
    /* Mengatur posisi teks di tengah */
    .centered-text {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40vh;
        font-size: 26px;
        font-weight: 500;
        text-align: center;
    }
    /* Mengatur kotak input dan tombol di bawah */
    .stTextInput {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        width: 85% !important;
        z-index: 100;
    }
    input {
        background-color: #212121 !important;
        border: 1px solid #424242 !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 15px 50px 15px 25px !important;
    }
    /* Sembunyikan elemen Streamlit yang tidak perlu */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Gaya untuk tombol tambahan (Simulasi) */
    .input-icons {
        position: fixed;
        bottom: 62px;
        right: 12%;
        display: flex;
        gap: 15px;
        z-index: 101;
        color: #b4b4b4;
    }
    </style>
    
    <div class="input-icons">
        <span>🎤</span>
        <span>⬆️</span>
    </div>
    """, unsafe_allow_html=True)

# Teks Utama di Tengah
st.markdown('<div class="centered-text">Ready when you are.</div>', unsafe_allow_html=True)

# Kotak Input di Bawah
query = st.text_input("", placeholder="Ask anything...", key="user_input")

# Tombol Kirim versi Streamlit agar fungsi berjalan
if st.button("Kirim Tanya"):
    if query:
        st.write("---")
        st.write(f"### Hasil untuk: {query}")
        
        # Logika Pencarian (Mahasiswa UNTRIB atau Google)
        try:
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
            
            if not hasil.empty:
                st.success("Data ditemukan!")
                st.table(hasil)
            else:
                url = f"https://api.duckduckgo.com/?q={query}&format=json"
                response = requests.get(url).json()
                if response.get("Abstract"):
                    if response.get("Image"):
                        st.image(f"https://duckduckgo.com{response['Image']}", width=300)
                    st.info(response["Abstract"])
                else:
                    st.write("Mencari informasi lebih lanjut di internet...")
        except:
            st.error("Sistem sedang memproses data...")
