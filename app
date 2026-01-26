import streamlit as st
import edge_tts
import asyncio
import os
import tempfile
import time

st.set_page_config(
    page_title="Pembuat Suara Indonesia",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Pembuat Suara Pria Logat Indonesia")

st.markdown("""
    Aplikasi ini memungkinkan Anda membuat audio dengan suara pria logat Indonesia. 
    Masukkan teks yang ingin diubah menjadi suara dan pilih suara pria Indonesia yang tersedia.
""")

# Sidebar untuk pengaturan
with st.sidebar:
    st.header("Pengaturan Suara")
    
    # Pilihan gaya suara
    voice_style = st.select_slider(
        "Gaya Bicara:",
        options=["Pelan", "Normal", "Cepat", "Bersemangat"],
        value="Normal"
    )
    
    # Pitch suara
    pitch_shift = st.slider(
        "Nada Suara:", 
        min_value=-10, 
        max_value=10, 
        value=0,
        help="Nilai minus untuk suara lebih rendah, nilai plus untuk suara lebih tinggi"
    )
    
    # Daftar suara pria Indonesia
    voice_options = {
        "Ardi (Pria Indonesia)": "id-ID-ArdiNeural",
    }
    
    # Tambahkan suara lainnya sebagai opsi
    other_voices = {
        "Thomas (Pria Melayu)": "ms-MY-OsmanNeural", 
        "Rizky (Pria Jawa Alternatif)": "jv-ID-DimasNeural",
        "Budi (Pria Sunda Alternatif)": "su-ID-JajangNeural"
    }
    
    # Gabungkan semua suara
    voice_options.update(other_voices)
    
    # Pilihan suara
    voice_name = st.selectbox(
        "Pilih Suara:", 
        list(voice_options.keys())
    )
    
    # Dapatkan kode suara berdasarkan pilihan
    selected_voice = voice_options[voice_name]
    
    # Tampilkan status
    st.info(f"Selected: {voice_name} ({selected_voice})")

# Fungsi untuk mendapatkan pengaturan berdasarkan gaya suara
def get_voice_settings(style, pitch):
    settings = {}
    
    # Atur kecepatan berdasarkan gaya
    if style == "Pelan":
        settings["rate"] = "-15%"
    elif style == "Normal":
        settings["rate"] = "+0%"
    elif style == "Cepat":
        settings["rate"] = "+15%"
    elif style == "Bersemangat":
        settings["rate"] = "+10%"
    
    # Atur pitch berdasarkan slider
    if pitch == 0:
        settings["pitch"] = "+0Hz"
    else:
        settings["pitch"] = f"{pitch:+d}Hz"
    
    # Atur volume
    if style == "Bersemangat":
        settings["volume"] = "+10%"
    else:
        settings["volume"] = "+0%"
    
    return settings

# Fungsi async untuk text-to-speech
async def generate_speech(text, voice, settings):
    try:
        # Buat file sementara untuk audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()
        output_file = temp_file.name
        
        # Buat komunikasi dengan edge-tts
        communicate = edge_tts.Communicate(
            text, 
            voice,
            rate=settings["rate"],
            volume=settings["volume"],
            pitch=settings["pitch"]
        )
        
        # Simpan ke file
        await communicate.save(output_file)
        
        return output_file, True
    except Exception as e:
        st.error(f"Error saat menghasilkan suara: {str(e)}")
        return "", False

# UI untuk input teks
st.subheader("Masukkan teks untuk diubah menjadi suara")
text_input = st.text_area(
    "Teks:",
    height=150,
    placeholder="Contoh: Halo, nama saya Ardi. Saya akan membacakan teks ini dengan logat Indonesia yang khas.",
    help="Masukkan teks yang ingin diubah menjadi suara"
)

# Informasi jumlah karakter
if text_input:
    char_count = len(text_input)
    st.caption(f"Jumlah karakter: {char_count}")

# Tombol untuk memulai proses
generate_btn = st.button("Buat Suara", type="primary", use_container_width=True)

# Jika tombol diklik
if generate_btn:
    if not text_input:
        st.error("Silakan masukkan teks terlebih dahulu!")
    else:
        with st.spinner("Sedang menghasilkan suara..."):
            # Dapatkan pengaturan suara
            voice_settings = get_voice_settings(voice_style, pitch_shift)
            
            # Tampilkan pengaturan yang digunakan
            st.info(f"Menggunakan pengaturan: Rate={voice_settings['rate']}, Pitch={voice_settings['pitch']}, Volume={voice_settings['volume']}")
            
            # Generate suara
            audio_file, success = asyncio.run(generate_speech(text_input, selected_voice, voice_settings))
            
            if success:
                st.success("Suara berhasil dibuat!")
                
                # Tampilkan audio player
                st.subheader("Hasil Audio")
                
                # Baca file audio
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                
                # Tampilkan audio player
                st.audio(audio_bytes, format="audio/mp3")
                
                # Tambahkan tombol unduh
                st.download_button(
                    label="Unduh Audio",
                    data=audio_bytes,
                    file_name=f"suara_indonesia_{int(time.time())}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
                
                # Hapus file sementara
                try:
                    os.remove(audio_file)
                except:
                    pass
            else:
                st.error("Gagal menghasilkan suara. Coba lagi dengan teks yang berbeda.")

# Informasi tambahan
with st.expander("Tentang Suara Pria Logat Indonesia"):
    st.markdown("""
    ### Informasi Suara
    
    Aplikasi ini menggunakan teknologi Edge TTS untuk menghasilkan suara dengan logat Indonesia yang natural.
    Suara-suara yang tersedia:
    
    - **Ardi (Pria Indonesia)**: Suara pria dewasa dengan logat Indonesia standar.
    - **Thomas (Pria Melayu)**: Suara pria dengan logat Melayu yang mirip dengan Indonesia.
    - **Rizky (Pria Jawa)**: Suara pria dengan logat Jawa Indonesia.
    - **Budi (Pria Sunda)**: Suara pria dengan logat Sunda Indonesia.
    
    ### Tips Penggunaan
    
    - Untuk hasil terbaik, gunakan kalimat lengkap dengan tanda baca.
    - Untuk pelafalan kata yang sulit, coba variasikan penulisannya.
    - Gunakan pengaturan pitch dan kecepatan untuk menyesuaikan karakter suara.
    """)

# Footer
st.markdown("---")
st.caption("Pembuat Suara Pria Logat Indonesia | Dibuat dengan ❤️ untuk content creator Indonesia")
