# =========================================
# ADAM ULTRA REALISTIC VOICE
# Human Pause + Breathing + Smart Rhythm
# =========================================

import streamlit as st
import edge_tts
import asyncio
import tempfile
import os
import random
import re
import time


# =========================================
# ADAM FIXED CONFIG (BEST SWEET SPOT)
# =========================================

VOICE = "id-ID-ArdiNeural"

BASE_RATE = -9     # tempo santai
BASE_PITCH = -5    # deep maskulin
VOLUME = "+0%"


# =========================================
# PAGE
# =========================================

st.set_page_config(
    page_title="Adam Ultra Realistic Voice",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Adam Voice – Ultra Realistic Mode")
st.caption("Deep • Natural • Breathing • Podcast • Human-like")


# =========================================
# HUMANIZER ENGINE (MAGIC DISINI)
# =========================================

def humanize_text(text: str):
    """
    Bikin suara kayak manusia:
    - jeda koma
    - jeda titik
    - jeda paragraf
    - napas random
    - ritme alami
    """

    text = re.sub(r"\s+", " ", text.strip())

    # jeda dasar
    text = text.replace(",", ", ... ")
    text = text.replace(".", ". ..... ")
    text = text.replace("\n", " ......... ")

    words = text.split()
    result = []

    for i, w in enumerate(words):
        result.append(w)

        # napas random tiap 10–18 kata
        if i > 5 and i % random.randint(10, 18) == 0:
            result.append("...")

    return " ".join(result)


def dynamic_rate(sentence):
    """
    Variasi tempo biar tidak flat
    """
    variation = random.randint(-2, 2)
    return f"{BASE_RATE + variation}%"


# =========================================
# TTS FUNCTION PER SENTENCE (BIAR LEBIH HIDUP)
# =========================================

async def generate(text):

    sentences = re.split(r'(?<=[.!?]) +', text)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()

    with open(temp_file.name, "wb") as final_audio:

        for sentence in sentences:

            if not sentence.strip():
                continue

            rate = dynamic_rate(sentence)

            pitch = f"{BASE_PITCH}Hz"

            communicate = edge_tts.Communicate(
                text=sentence,
                voice=VOICE,
                rate=rate,
                pitch=pitch,
                volume=VOLUME
            )

            part_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            part_file.close()

            await communicate.save(part_file.name)

            with open(part_file.name, "rb") as pf:
                final_audio.write(pf.read())

            os.remove(part_file.name)

    return temp_file.name


# =========================================
# UI
# =========================================

st.subheader("Masukkan Teks")

text = st.text_area(
    "",
    height=220,
    placeholder="Halo teman-teman. Hari ini saya akan membahas sesuatu yang sangat penting untuk masa depan kalian..."
)

if text:
    st.caption(f"{len(text)} karakter")


if st.button("🎙️ Generate Adam Ultra Realistic", use_container_width=True):

    if not text:
        st.warning("Masukkan teks dulu")
        st.stop()

    with st.spinner("Generating ultra realistic voice..."):

        processed = humanize_text(text)

        file_path = asyncio.run(generate(processed))

        with open(file_path, "rb") as f:
            audio = f.read()

        st.success("Selesai! Suara sangat natural 🎧")

        st.audio(audio)

        st.download_button(
            "⬇️ Download MP3",
            audio,
            file_name=f"adam_ultra_{int(time.time())}.mp3",
            mime="audio/mp3",
            use_container_width=True
        )

        os.remove(file_path)


# =========================================
# INFO
# =========================================

st.markdown("---")

st.info("""
🔥 Ultra Realistic aktif:
✅ Auto pause
✅ Napas manusia
✅ Variasi tempo
✅ Tidak robotik
✅ Podcast vibe

Setting:
Voice : Ardi Neural
Rate  : sekitar -9% (dinamis)
Pitch : -5Hz
""")
