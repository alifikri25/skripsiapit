import streamlit as st
import pandas as pd
import time
import os
from crypto_utils import aes_encrypt, aes_decrypt, rc6_encrypt, rc6_decrypt

st.set_page_config(page_title="Sistem Uji Kriptografi", layout="wide")

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

page_selection = st.sidebar.radio(
    "Navigasi Utama", 
    nav_options,
    index=current_index
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

# --- Page Routing ---
page = st.session_state.current_page

if page == "Beranda":
    # Sesuai Sketsa 1 Area Kanan
    st.title("Perbandingan Kinerja Algoritma")
    st.header("Advanced Encryption Standard (AES)")
    st.header("Rivest Cipher 6 (RC6)")
    
    st.markdown("---")
    st.write("Aplikasi pengujian performa algoritma kriptografi. Anda dapat beralih ke halaman **Menu** (lewat bilah di pinggir kiri) untuk berpindah ke area eksekusi uji materi pengolahan file.")

elif page == "Menu":
    st.title("Pilihan Ruang Uji")
    st.write("Silakan pilih mode pengujian yang ingin Anda lakukan secara spesifik saat ini:")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col_space, col2 = st.columns([4, 1, 4])
    
    with col1:
        st.markdown(
            """
            <div style='border: 2px solid #555; padding: 60px; text-align: center; border-radius: 10px; background-color: #f9f9f9;'>
                <h1 style='color: #333;'>ENKRIPSI</h1>
            </div>
            <br>
            """, unsafe_allow_html=True
        )
        if st.button("Masuk Halaman Enkripsi", use_container_width=True, type="primary"):
            go_to_page("  - Enkripsi")
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style='border: 2px solid #555; padding: 60px; text-align: center; border-radius: 10px; background-color: #f9f9f9;'>
                <h1 style='color: #333;'>DEKRIPSI</h1>
            </div>
            <br>
            """, unsafe_allow_html=True
        )
        if st.button("Masuk Halaman Dekripsi", use_container_width=True, type="primary"):
            go_to_page("  - Dekripsi")
            st.rerun()

elif page == "  - Enkripsi":
    # Sesuai Sketsa 2
    st.title("Proses Enkripsi Tunggal")
    st.markdown("Unggah **1 (Tunggal)** file asli untuk simulasi enkripsi. Anda harus mengujinya satu-satu untuk mendapatkan data ukuran dan rekap jejak performa web pada Tabel Akhir.")
    
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
                st.dataframe(pd.DataFrame([record]))
                
            except Exception as e:
                st.error(f"Terjadi kesalahan parah saat enkripsi: {e}")

elif page == "  - Dekripsi":
    # Sesuai Sketsa Dekripsi
    st.title("Proses Dekripsi Tunggal")
    st.markdown("Unggah **1 (Tunggal)** file *Sandi/Ciphertext* hasil download dari pengujian Anda sebelumnya untuk dikembalikan menjadi file dokumen utuh. Kunci harus 100% kongruen (identik).")
    
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
                    st.dataframe(pd.DataFrame([record]))
                else:
                    st.error("Gagal Dekripsi! Proses ditolak. Menelaah blok palsu. Kesalahan ini biasanya bersumber dari ketidaksesuaian 'KUNCI' atau algoritma dekriptornya berlainan spesies.")
            except Exception as e:
                st.error(f"Gagal Total Dekripsi! Kunci pasti salah, algoritma tertukar/salah sandar, atau Anda memakai file rusak. Error Log System: {e}")

elif page == "Tabel Akhir":
    st.title("Tabel Akhir (Master Rekapitulasi)")
    
    # Syarat mutlak: minimal telah mencetak skor 1 x di arena Enkrips dan Dekripsi
    has_enc_data = len(st.session_state.enc_history) > 0
    has_dec_data = len(st.session_state.dec_history) > 0
    
    if not (has_enc_data and has_dec_data):
        st.warning("Papan Tabel Akhir di-disabled (Terkunci) sementara hingga tuntasnya proses. Pastikan Anda telah mengarungi/menyelesaikan minimal 1 simulasi penulisan Enkripsi beserta 1 operasi kembar Dekripsi terlebih dahulu. Saat ini sistem merasakan ada rantai uji yang bolong.")
    else:
        st.success("Tabel Pengamatan Terbuka Penuh. Seluruh parameter uji berjejer dikumpulkan layaknya skenario (One-by-One / Single Push). File Anda disajikan berurut:")
        
        # Sedot memori dataframes (Akumulasi List Global Array)
        df_enc = pd.DataFrame(st.session_state.enc_history)
        df_dec = pd.DataFrame(st.session_state.dec_history)
        
        st.markdown("---")
        st.header("Rekapitulasi Konsistensi Kecepatan: Proses **ENKRIPSI**")
        st.dataframe(df_enc, use_container_width=True)
        csv_enc = df_enc.to_csv(index=False).encode('utf-8')
        st.download_button("Ekstrak Laporan Semua Tabel Enkripsi (CSV)", data=csv_enc, file_name="Master_Tabel_Akhir_Enkripsi.csv", mime="text/csv")
        
        st.markdown("---")
        st.header("Rekapitulasi Konsistensi Kecepatan: Proses **DEKRIPSI**")
        st.dataframe(df_dec, use_container_width=True)
        csv_dec = df_dec.to_csv(index=False).encode('utf-8')
        st.download_button("Ekstrak Laporan Semua Tabel Dekripsi (CSV)", data=csv_dec, file_name="Master_Tabel_Akhir_Dekripsi.csv", mime="text/csv")
