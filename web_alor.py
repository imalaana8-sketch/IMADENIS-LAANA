import streamlit as st
import pandas as pd

# Mengatur tampilan halaman web
st.set_page_config(page_title="Alor.GPT", page_icon="🤖")

# Judul Aplikasi
st.title("🤖 Alor.GPT Web")
st.write("Sistem Cerdas Universitas Tribuana Kalabahi")
st.markdown("---")

# Pilihan Menu
menu = st.radio("Pilih Mode Pencarian:", ["Cari Data Mahasiswa UNTRIB", "Cari di Google"])

# Kotak Input (seperti kotak chat AI)
query = st.text_input("Ketikkan pencarian...", placeholder="Misal: Nama, NIM, atau pertanyaan...")

# Tombol Cari
if st.button("Kirim"):
    if query:
        if menu == "Cari Data Mahasiswa UNTRIB":
            try:
                # Membaca database CSV
                df = pd.read_csv("mahasiswa_untrib.csv")
                
                # Mencari data (huruf kecil/besar bebas)
                pencarian = df[
                    df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
                ]
                
                if not pencarian.empty:
                    st.success("✅ Data Ditemukan!")
                    # Menampilkan data dalam bentuk tabel web yang rapi
                    st.dataframe(pencarian, use_container_width=True)
                else:
                    st.warning("⚠️ Data mahasiswa tidak ditemukan.")
            except FileNotFoundError:
                st.error("File mahasiswa_untrib.csv tidak ditemukan di folder ini.")
        
        elif menu == "Cari di Google":
            st.info(f"🔍 Mencari informasi tentang: **{query}**")
            st.write("*(Simulasi)*: Sistem berhasil menerima perintah pencarian Google. Kita akan sambungkan fungsinya di tahap selanjutnya!")
    else:
        st.error("Silakan ketik sesuatu terlebih dahulu.")