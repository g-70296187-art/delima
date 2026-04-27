import streamlit as st
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Semakan DELIMA 1IB",
    page_icon="🎓",
    layout="centered"
)

# 2. GAYA VISUAL (CSS) - Untuk mencantikkan UI
st.markdown("""
    <style>
    /* Tukar warna background utama */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Cantikkan kotak input */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #007bff;
        padding: 10px 20px;
        font-size: 18px;
    }
    /* Cantikkan kad maklumat */
    .stAlert {
        border-radius: 15px;
    }
    /* Tajuk Center */
    .main-title {
        text-align: center;
        color: #1a237e;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LINK DATA (Gunakan link CSV Google Sheets anda)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRyKqWvNqanWnfzc967HrImHjJ28K4i5JcoNars0PrQDe3pu9gmoz7Cxs1eQj63vAvOx80fox5TlnFU/pub?gid=376187573&single=true&output=csv"

# 4. FUNGSI MUAT DATA
@st.cache_data(ttl=600) # Simpan data dalam cache selama 10 minit
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        # Pastikan semua data teks adalah huruf besar untuk carian konsisten
        df = df.apply(lambda x: x.astype(str).str.upper() if x.dtype == "object" else x)
        return df
    except Exception as e:
        return None

# 5. HEADER & VISUAL ATAS
st.markdown("<h1 class='main-title'>🔍 SISTEM SEMAKAN ID DELIMA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Masukkan nama anda untuk mendapatkan ID & Maklumat Kelas secara pantas.</p>", unsafe_allow_html=True)
st.divider()

# 6. LOGIK APLIKASI
data = load_data()

if data is not None:
    # Kotak Carian
    nama_input = st.text_input("", placeholder="TAIP NAMA PENUH ANDA DI SINI...").strip().upper()

    if nama_input:
        if len(nama_input) < 3:
            st.info("💡 Sila taip sekurang-kurangnya 3 abjad untuk memulakan carian.")
        else:
            # Tapis data berdasarkan nama (Lajur pertama)
            # Anda boleh tukar 'NAMA' kepada nama header sebenar dalam sheet anda
            hasil = data[data.iloc[:, 0].str.contains(nama_input, na=False)]

            if not hasil.empty:
                st.balloons() # Animasi kejayaan
                st.success(f"✅ Menjumpai {len(hasil)} rekod yang sepadan.")
                
                # Paparkan dalam bentuk DataFrame/Jadual yang kemas
                # Kita hanya tunjuk 3 kolum pertama (Nama, ID, Kelas)
                st.dataframe(
                    hasil.iloc[:, :3], 
                    use_container_width=True,
                    hide_index=True
                )
                
                st.info("📌 **Nota:** Sila simpan/salin ID anda untuk kegunaan rasmi.")
            else:
                st.error("❌ Nama tidak dijumpai. Sila pastikan ejaan mengikut IC atau hubungi Guru Kelas.")
    else:
        # Paparan semasa kotak carian kosong
        st.write("")
        st.info("Selamat Datang! Sila gunakan kotak carian di atas.")
        
        # Tambah statistik ringkas di bawah
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Jumlah Rekod Murid", value=len(data))
        with c2:
            st.metric(label="Status Sistem", value="AKTIF")

else:
    st.error("⚠️ Ralat teknikal: Gagal menyambung ke pangkalan data Google Sheets. Sila cuba sebentar lagi.")

# 7. FOOTER
st.divider()
st.markdown("""
    <div style='text-align: center; font-size: 12px; color: #888;'>
        Sistem Semakan Kendiri &copy; 2026 | Dikembangkan untuk memudahkan urusan murid.
    </div>
    """, unsafe_allow_html=True)
