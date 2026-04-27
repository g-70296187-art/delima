import streamlit as st
import pandas as pd

st.set_page_config(page_title="Semakan DELIMA", layout="wide")

# CSS Khas untuk mencantikkan lagi UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 10px;
        border: 2px solid #1E88E5;
    }
    </style>
    """, unsafe_allow_html=True)

CSV_URL = "URL_GOOGLE_SHEETS_ANDA"

def load_data():
    return pd.read_csv(CSV_URL)

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>🔍 SEMAKAN ID DELIMA BERSATU</h1>", unsafe_allow_html=True)
st.divider()

try:
    df = load_data()
    
    # Bahagian Carian dalam Kolum
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        nama_cari = st.text_input("MASUKKAN NAMA PENUH ANDA:", placeholder="Contoh: AHMAD ZAKI").strip().upper()

    if len(nama_cari) >= 3:
        hasil = df[df.iloc[:, 0].str.contains(nama_cari, case=False, na=False)]
        
        if not hasil.empty:
            st.balloons() # Animasi gembira bila jumpa!
            st.success(f"Padanan dijumpai: {len(hasil)} rekod")
            
            # Paparan data dalam bentuk table yang cantik
            st.table(hasil.iloc[:, :3]) 
        else:
            st.error("Nama tidak dijumpai. Sila cuba lagi.")
            
except Exception as e:
    st.warning("Menunggu data dari Google Sheets...")

st.sidebar.title("Bantuan")
st.sidebar.info("Sistem ini memudahkan murid menyemak ID tanpa perlu mencari dalam senarai panjang.")
