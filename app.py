import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Semakan DELIMA 2026 - SMKTBR1",
    page_icon="🎓",
    layout="centered"
)

# 2. GAYA VISUAL (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #800000;
    }
    .main-title {
        text-align: center;
        color: #800000;
        font-family: 'Arial Black', Gadget, sans-serif;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #333;
        font-weight: bold;
        margin-top: 0px;
    }
    .year-badge {
        text-align: center;
        color: #ffffff;
        background-color: #800000;
        border-radius: 5px;
        padding: 2px 10px;
        display: inline-block;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. PAPARAN LOGO & NAMA SEKOLAH
if os.path.exists("logo.jpg"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        image = Image.open("logo.jpg")
        st.image(image, width=150)
        layout="centered"

st.markdown("<h1 class='main-title'>SMK TAMAN BUNGA RAYA 1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><span class='year-badge'>SESI 2026</span></p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>SISTEM SEMAKAN ID DELIMA MURID</p>", unsafe_allow_html=True)
st.divider()

# 4. LINK DATA
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyKqWvNqanWnfzc967HrImHjJ28K4i5JcoNars0PrQDe3pu9gmoz7Cxs1eQj63vAvOx80fox5TlnFU/pub?gid=376187573&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        return None

# 5. LOGIK CARIAN
data = load_data()

if data is not None:
    nama_input = st.text_input("MASUKKAN NAMA PENUH ANDA:", placeholder="Contoh: MUHAMMAD ALI BIN OSMAN").strip().upper()

    if nama_input:
        if len(nama_input) < 3:
            st.warning("⚠️ Sila taip sekurang-kurangnya 3 huruf untuk mencari.")
        else:
            hasil = data[data.iloc[:, 0].astype(str).str.contains(nama_input, case=False, na=False)]

            if not hasil.empty:
                st.balloons()
                st.success(f"Rekod Ditemui: {len(hasil)}")
                st.dataframe(
                    hasil.iloc[:, :3], 
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.error("Tiada rekod ditemui. Sila pastikan ejaan betul atau hubungi Guru Kelas.")
    else:
        st.info("Sila masukkan nama untuk memulakan semakan sesi 2026.")

else:
    st.error("Gagal memuatkan data. Sila semak pautan Google Sheets anda.")

# 6. FOOTER
st.divider()
st.markdown("<p style='text-align: center; font-size: 12px;'>&copy; 2026 SMK Taman Bunga Raya 1 | Berilmu, Berdisiplin, Berbakti</p>", unsafe_allow_html=True)
