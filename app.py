import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Semakan ID DELIMA", page_icon="🔍")

# Link CSV Google Sheets anda
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyKqWvNqanWnfzc967HrImHjJ28K4i5JcoNars0PrQDe3pu9gmoz7Cxs1eQj63vAvOx80fox5TlnFU/pub?gid=376187573&single=true&output=csv"

st.title("🔍 Sistem Semakan ID DELIMA")
st.write("Sila masukkan nama anda untuk menyemak ID dan Kelas.")

# Fungsi muat data
@st.cache_data(ttl=300) # Data disimpan selama 5 minit sebelum refresh automatik
def load_data():
    return pd.read_csv(CSV_URL)

try:
    df = load_data()
    
    # Kotak Carian yang besar dan mesra pengguna
    nama_cari = st.text_input("TAIP NAMA PENUH ANDA:", "").strip().upper()

    if len(nama_cari) >= 3:
        # Tapis data (Cari dalam lajur 'NAMA')
        # Nota: Pastikan tajuk lajur dalam Google Sheets anda adalah 'NAMA'
        hasil = df[df.iloc[:, 0].str.contains(nama_cari, case=False, na=False)]
        
        if not hasil.empty:
            st.success(f"Menjumpai {len(hasil)} rekod.")
            # Paparkan Nama, ID, dan Kelas sahaja (3 kolum pertama)
            st.dataframe(hasil.iloc[:, :3], use_container_width=True)
        else:
            st.warning("Tiada padanan dijumpai. Sila pastikan ejaan betul.")
    elif len(nama_cari) > 0:
        st.info("Sila taip sekurang-kurangnya 3 huruf.")

except Exception as e:
    st.error("Gagal memuatkan data dari Google Sheets. Sila hubungi admin.")

st.divider()
st.caption("Data dikemaskini secara langsung dari Google Sheets.")