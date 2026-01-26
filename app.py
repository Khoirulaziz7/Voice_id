# =========================================
# ADAM VOICE ONLY – Indonesian TTS
# Clean • Simple • ElevenLabs Style
# =========================================

import streamlit as st
import edge_tts
import asyncio
import tempfile
import os
import re
import time


# =========================================
# CONFIG ADAM (FIXED - TIDAK BISA DIUBAH)
# =========================================

VOICE = "id-ID-ArdiNeural"

ADAM_SETTINGS = {
    "rate": "-9%",     # tempo santai
    "pitch": "-5Hz",   # deep maskulin
    "volume": "+0%"
}


# =========================================
# PAGE
# =========================================

st.set_page_config(
    page_title="Adam Voice Indonesia",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Adam Voice Indonesia")
st.caption("Deep • Natural • Podcast • Mirip ElevenLabs Adam")


# =========================================
# AUTO NATURAL PAUSE
# =========================================

def enhance_text(text: str):
    text = re.sub(r",", ", ... ", text)
    text = re.sub(r"\.", ". ... ", text)
    text = re.sub(r"\n", " ... ", text)
    return text


# =========================================
# TTS FUNCTION
# =========================================

async def generate(text):

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp.close()

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=ADAM_SETTINGS["rate"],
        volume=ADAM_SETTINGS["volume"],
        pitch=ADAM_SETTINGS["pitch"]
    )

    await communicate.save(temp.name)

    return temp.name


# =========================================
# UI
# =========================================

st.subheader("Masukkan Teks")

text = st.text_area(
    "",
    height=200,
    placeholder="Halo teman-teman. Hari ini saya akan membahas sesuatu yang menarik..."
)

if text:
    st.caption(f"{len(text)} karakter")


if st.button("🎙️ Generate Adam Voice", use_container_width=True):

    if not text:
        st.warning("Masukkan teks dulu")
        st.stop()

    with st.spinner("Generating Adam voice..."):

        processed = enhance_text(text)

        file_path = asyncio.run(generate(processed))

        with open(file_path, "rb") as f:
            audio = f.read()

        st.audio(audio)

        st.download_button(
            "⬇️ Download MP3",
            audio,
            file_name=f"adam_voice_{int(time.time())}.mp3",
            mime="audio/mp3",
            use_container_width=True
        )

        os.remove(file_path)


# =========================================
# INFO
# =========================================

st.markdown("---")

st.info("""
⚙️ Setting otomatis:
• Voice : Ardi Neural  
• Rate  : -9%  
• Pitch : -5Hz  
• Style : Podcast Deep (Adam ElevenLabs)

Tips:
Gunakan koma, titik, atau "..." untuk jeda natural.
""")
