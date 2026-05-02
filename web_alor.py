import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Alor.GPT - UNTRIB", layout="wide")

st.title("Alor.GPT 🚀")
st.write("Sistem Informasi Mahasiswa Universitas Tribuana Kalabahi")

# Mode Pencarian
mode = st.radio("Pilih Mode Pencarian:", ["Cari Data Mahasiswa UNTRIB", "Cari di Google"])

query = st.text_input("Ketikkkan pencarian...")
tombol = st.button("Kirim")

if tombol and query:
    if mode == "Cari di Google":
        st.subheader(f"🔎 Hasil Pencarian untuk: {query}")
        
        # Menggunakan API DuckDuckGo (Gratis dan Mudah untuk Pemula)
        url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        response = requests.get(url).json()
        
        # Menampilkan Gambar Utama jika ada
        if response.get("Image"):
            st.image(f"https://duckduckgo.com{response['Image']}", caption=query, width=300)
        
        # Menampilkan Deskripsi/Abstrak
        if response.get("Abstract"):
            st.info(response["Abstract"])
            st.write(f"Sumber: {response.get('AbstractURL')}")
        else:
            st.warning("Maaf, detail teks tidak ditemukan. Coba kata kunci lain.")
            
        # Menampilkan Topik Terkait (Related Topics)
        st.write("---")
        st.write("### Topik Terkait:")
        for topic in response.get("RelatedTopics", [])[:3]:
            if "Text" in topic:
                st.write(f"- {topic['Text']}")

    elif mode == "Cari Data Mahasiswa UNTRIB":
        # Bagian ini mengambil data dari file csv yang sudah kamu upload di GitHub
        try:
            df = pd.read_csv("mahasiswa_untrib.csv")
            hasil = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
            
            if not hasil.empty:
                st.success(f"Ditemukan {len(hasil)} data mahasiswa!")
                st.table(hasil)
            else:
                st.error("Data mahasiswa tidak ditemukan.")
        except:
            st.error("File mahasiswa_untrib.csv tidak ditemukan di server.")
