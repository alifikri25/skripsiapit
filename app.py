import streamlit as st
import pandas as pd
import time
import os
from crypto_utils import aes_encrypt, aes_decrypt, rc6_encrypt, rc6_decrypt

st.set_page_config(page_title="Sistem Uji Kriptografi", layout="wide")

# --- Global CSS: Warna & Background ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e8eaf6 0%, #ede7f6 50%, #e3f2fd 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1565c0 0%, #0d47a1 50%, #1a237e 100%) !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div {
        color: white !important;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.2) !important; }
    [data-testid="stSidebar"] button { background-color: #e53935 !important; color: white !important; border: none !important; }
    .main .block-container {
        background: rgba(255,255,255,0.88);
        border-radius: 20px;
        padding: 2rem 3rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Global Session State ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"
if 'enc_history' not in st.session_state:
    st.session_state.enc_history = []
if 'dec_history' not in st.session_state:
    st.session_state.dec_history = []

# --- Helper Functions ---
def go_to_page(page_name):
    st.session_state.current_page = page_name

def get_algo_func(algo_name, mode):
    if algo_name == "Advanced Encryption Standard (AES)":
        return aes_encrypt if mode == "encrypt" else aes_decrypt
    else:
        return rc6_encrypt if mode == "encrypt" else rc6_decrypt

# --- Navigation Sidebar ---
st.sidebar.title("Kriptografi")

# Tentukan menu navigasi hirarki bapak dan anak
nav_options = ["Beranda", "Menu", "  - Enkripsi", "  - Dekripsi", "Tabel Akhir"]
current_index = nav_options.index(st.session_state.current_page) if st.session_state.current_page in nav_options else 0

def format_nav(opt):
    icons = {"Beranda": "🏠 Beranda", "Menu": "📋 Menu", "  - Enkripsi": "  🔐 Enkripsi", "  - Dekripsi": "  🔓 Dekripsi", "Tabel Akhir": "📊 Tabel Akhir"}
    return icons.get(opt, opt)

page_selection = st.sidebar.radio(
    "Navigasi Utama", 
    nav_options,
    index=current_index,
    format_func=format_nav
)

# Jika diklik di sidebar, sync dengan session state
if page_selection != st.session_state.current_page:
    st.session_state.current_page = page_selection
    st.rerun()

# Tombol rahasia untuk mereset seluruh history (untuk testing ulang keseluruhan skripsi)
st.sidebar.markdown("---")
if st.sidebar.button("Reset Seluruh History Pengujian (Mulai Awal)"):
    st.session_state.enc_history = []
    st.session_state.dec_history = []
    st.session_state.current_page = "Beranda"
    st.rerun()

# Profil Mahasiswa
st.sidebar.markdown(
    """
    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.25);">
        <p style="margin: 0; font-size: 13px; color: rgba(255,255,255,0.8);"><b>Dikembangkan oleh:</b></p>
        <p style="margin: 0; font-size: 16px; font-weight: bold; color: #ffffff;">Hafidz Maulana Rahman</p>
        <p style="margin: 0; font-size: 14px; color: rgba(255,255,255,0.8);">NPM: 202210715069</p>
    </div>
    """, unsafe_allow_html=True
)

# --- Page Routing ---
page = st.session_state.current_page

if page == "Beranda":
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 35px; border-radius: 20px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 40px rgba(102,126,234,0.4);">
            <h1 style="color: white; margin-bottom: 15px; font-size: 30px; font-weight: 400; letter-spacing: 2px;">PERBANDINGAN KINERJA ALGORITMA</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 8px 0; font-size: 20px; font-weight: 300;">Advanced Encryption Standard (AES)</p>
            <p style="color: rgba(255,255,255,0.9); margin: 8px 0; font-size: 20px; font-weight: 300;">Rivest Cipher 6 (RC6)</p>
            <p style="color: rgba(255,255,255,0.7); margin-top: 15px; font-size: 18px; font-weight: 300;">128-bit</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("Aplikasi pengujian performa algoritma kriptografi. Anda dapat beralih ke halaman **Menu** untuk berpindah ke area eksekusi uji materi pengolahan file.")

elif page == "Menu":
    st.markdown("<h1 style='text-align: center; color: #333;'>Pilihan Ruang Uji</h1><hr>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col_space, col2 = st.columns([4, 1, 4])
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #7c4dff 0%, #b388ff 100%); padding: 60px 30px; text-align: center; border-radius: 15px; box-shadow: 0 10px 30px rgba(124,77,255,0.3);'>
                <h1 style='color: white; margin: 0;'>🔐 Enkripsi</h1>
                <p style='color: rgba(255,255,255,0.8); margin-top: 10px;'>AES & RC6</p>
            </div><br>""", unsafe_allow_html=True)
        if st.button("Masuk Halaman Enkripsi", use_container_width=True, type="primary"):
            go_to_page("  - Enkripsi")
            st.rerun()
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #7c4dff 0%, #b388ff 100%); padding: 60px 30px; text-align: center; border-radius: 15px; box-shadow: 0 10px 30px rgba(124,77,255,0.3);'>
                <h1 style='color: white; margin: 0;'>🔓 Dekripsi</h1>
                <p style='color: rgba(255,255,255,0.8); margin-top: 10px;'>AES & RC6</p>
            </div><br>""", unsafe_allow_html=True)
        if st.button("Masuk Halaman Dekripsi", use_container_width=True, type="primary"):
            go_to_page("  - Dekripsi")
            st.rerun()

elif page == "  - Enkripsi":
    # Sesuai Sketsa 2
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e88e5 0%, #5e35b1 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(94,53,177,0.3);">
            <h1 style="color: white; margin: 0;">🔐 Proses Enkripsi</h1>
        </div>""", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Unggah <b>1 (Satu)</b> file asli untuk simulasi enkripsi. Anda harus mengujinya satu-satu untuk mendapatkan data ukuran dan rekap jejak performa web pada Tabel Akhir.</p>", unsafe_allow_html=True)
    
    # 1. Dropfile
    uploaded_file = st.file_uploader("Upload File Asli", accept_multiple_files=False)
    
    # 2. Choose Algorithm
    algo = st.selectbox("Pilih Algoritma", ["Advanced Encryption Standard (AES)", "Rivest Cipher 6 (RC6)"])
    
    # 3. Key
    key_input = st.text_input("Kunci Rahasia (Wajib pas 16 Karakter / 128-bit)", type="password")
    
    # 4. Mulai
    if st.button("Mulai Proses Enkripsi", type="primary"):
        if not uploaded_file:
            st.error("Masukkan (Drop) file terlebih dahulu!")
            st.stop()
        if len(key_input) != 16:
            st.error(f"Kunci yang dimasukkan memiliki {len(key_input)} karakter. Wajib mutlak 16 karakter!")
            st.stop()
            
        with st.spinner("Sistem memproses komputasi algoritma..."):
            file_bytes = uploaded_file.read()
            original_mb = len(file_bytes) / 1048576
            key_bytes = key_input.encode('utf-8')
            
            # Eksekusi Enkripsi
            func_enc = get_algo_func(algo, "encrypt")
            start_t = time.time()
            try:
                ct = func_enc(file_bytes, key_bytes)
                end_t = time.time()
                enc_time = end_t - start_t
                throughput = original_mb / enc_time if enc_time > 0 else 0
                
                # Append to history memory
                record = {
                    "Jenis File": os.path.splitext(uploaded_file.name)[1].lower().replace('.', ''),
                    "Size (MB)": round(original_mb, 6),
                    "Algoritma": algo,
                    "Waktu (s)": round(enc_time, 5),
                    "Throughput (MB/s)": round(throughput, 4)
                }
                st.session_state.enc_history.append(record)
                
                st.success("Enkripsi Berhasil Diesksekusi! Ingatan parameter ini sudah dilesapkan ke Tabel Akhir.")
                
                # 5. Simpan hasil File enkrip
                st.download_button(
                    label="Simpan Hasil File Enkripsi (Teks Sandi)",
                    data=ct,
                    file_name=f"ENCRYPTED_{uploaded_file.name}",
                    mime="application/octet-stream"
                )
                
                # Show Table Layout untuk individu file ini
                st.write("Tabel Hasil Individual Saat Ini:")
                df_single = pd.DataFrame([record])
                df_single.index = [1]
                st.dataframe(df_single)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan parah saat enkripsi: {e}")

elif page == "  - Dekripsi":
    # Sesuai Sketsa Dekripsi
    st.markdown("""
        <div style="background: linear-gradient(135deg, #00897b 0%, #1565c0 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(21,101,192,0.3);">
            <h1 style="color: white; margin: 0;">🔓 Proses Dekripsi</h1>
        </div>""", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Unggah <b>1 (Satu)</b> file <i>Sandi/Ciphertext</i> hasil download dari pengujian Anda sebelumnya untuk dikembalikan menjadi file dokumen utuh.</p>", unsafe_allow_html=True)
    
    # 1. Dropfile (Khusus Hasil)
    uploaded_file = st.file_uploader("Upload File Teks Sandi (Hasil dari Enkripsi)", accept_multiple_files=False)
    
    # 2. Choose Algorithm
    algo = st.selectbox("Pilih Algoritma Rekonstruksi", ["Advanced Encryption Standard (AES)", "Rivest Cipher 6 (RC6)"])
    
    # 3. Key
    key_input = st.text_input("Kunci Rahasia Pembuka (Wajib pas 16 Karakter / 128-bit)", type="password")
    
    # 4. Mulai Dekrip
    if st.button("Mulai Proses Dekripsi", type="primary"):
        if not uploaded_file:
            st.error("Masukkan (Drop) file sandi/ciphertext terlebih dahulu!")
            st.stop()
        if len(key_input) != 16:
            st.error(f"Kunci uji Anda {len(key_input)} karakter. Ia wajib persis 16 karakter!")
            st.stop()
            
        with st.spinner("Mesin berusaha merobohkan dan memulihkan sandi komputasi..."):
            file_bytes = uploaded_file.read()
            original_mb = len(file_bytes) / 1048576
            key_bytes = key_input.encode('utf-8')
            
            func_dec = get_algo_func(algo, "decrypt")
            start_t = time.time()
            try:
                pt = func_dec(file_bytes, key_bytes)
                end_t = time.time()
                dec_time = end_t - start_t
                throughput = original_mb / dec_time if dec_time > 0 and len(pt) > 0 else 0
                
                # Coba cabut ekstensi kotor dari .mp4 misal ENCRYPTED_file.mp4 (kalau bisa)
                ext_asli = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')
                clean_name = uploaded_file.name.replace("ENCRYPTED_", "")
                if clean_name == uploaded_file.name: 
                    clean_name = "DECRYPTED_" + uploaded_file.name

                record = {
                    "Jenis File": ext_asli,
                    "Size (MB)": round(original_mb, 6),
                    "Algoritma": algo,
                    "Waktu (s)": round(dec_time, 5),
                    "Throughput (MB/s)": round(throughput, 4)
                }
                
                if len(pt) > 0: # Valid decryption check (karena RC6 pure error bytes akan terbaca)
                    st.session_state.dec_history.append(record)
                    st.success("Dekripsi Berhasil! File sanggup dikembalikan ke wujud orisinil. Rekap tercatat dengan aman.")
                    
                    # 5. Simpan hasil File Dekrip
                    st.download_button(
                        label="Simpan Hasil File Dekripsi (Kembali Original)",
                        data=pt,
                        file_name=clean_name,
                        mime="application/octet-stream"
                    )
                    
                    st.write("Tabel Hasil Individual Saat Ini:")
                    df_single = pd.DataFrame([record])
                    df_single.index = [1]
                    st.dataframe(df_single)
                else:
                    st.error("Gagal Dekripsi! Proses ditolak. Menelaah blok palsu. Kesalahan ini biasanya bersumber dari ketidaksesuaian 'KUNCI' atau algoritma dekriptornya berlainan spesies.")
            except Exception as e:
                st.error(f"Gagal Total Dekripsi! Kunci pasti salah, algoritma tertukar/salah sandar, atau Anda memakai file rusak. Error Log System: {e}")

elif page == "Tabel Akhir":
    st.markdown("""
        <div style="background: linear-gradient(135deg, #7b1fa2 0%, #4a148c 100%); padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(123,31,162,0.3);">
            <h1 style="color: white; margin: 0;">📊 Tabel Akhir Proses Kriptografi</h1>
        </div>""", unsafe_allow_html=True)
    
    # Syarat mutlak: minimal telah mencetak skor 1 x di arena Enkrips dan Dekripsi
    has_enc_data = len(st.session_state.enc_history) > 0
    has_dec_data = len(st.session_state.dec_history) > 0
    
    if not (has_enc_data and has_dec_data):
        st.warning("Papan Tabel Akhir di-disabled (Terkunci) sementara hingga tuntasnya proses. Pastikan Anda telah mengarungi/menyelesaikan minimal 1 simulasi penulisan Enkripsi beserta 1 operasi kembar Dekripsi terlebih dahulu. Saat ini sistem merasakan ada rantai uji yang bolong.")
    else:
        st.success("Tabel Pengamatan Terbuka Penuh. Seluruh parameter uji berjejer dikumpulkan layaknya skenario (One-by-One / Single Push). File Anda disajikan berurut:")
        
        # Sedot memori dataframes (Akumulasi List Global Array)
        df_enc = pd.DataFrame(st.session_state.enc_history)
        if not df_enc.empty: df_enc.index = range(1, len(df_enc) + 1)
        
        df_dec = pd.DataFrame(st.session_state.dec_history)
        if not df_dec.empty: df_dec.index = range(1, len(df_dec) + 1)
        
        st.markdown("---")
        st.markdown("<h3 style='text-align: center; color: #c62828;'>Tabel Enkripsi</h3>", unsafe_allow_html=True)
        st.dataframe(df_enc, use_container_width=True)
        csv_enc = df_enc.to_csv(index=False).encode('utf-8')
        st.download_button("Ekstrak Laporan Semua Tabel Enkripsi (CSV)", data=csv_enc, file_name="Master_Tabel_Akhir_Enkripsi.csv", mime="text/csv")
        
        st.markdown("---")
        st.markdown("<h3 style='text-align: center; color: #1565c0;'>Tabel Dekripsi</h3>", unsafe_allow_html=True)
        st.dataframe(df_dec, use_container_width=True)
        csv_dec = df_dec.to_csv(index=False).encode('utf-8')
        st.download_button("Ekstrak Laporan Semua Tabel Dekripsi (CSV)", data=csv_dec, file_name="Master_Tabel_Akhir_Dekripsi.csv", mime="text/csv")
