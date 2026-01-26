# =========================================
# ADAM VOICE – FINAL CLEAN STABLE VERSION
# Human Pause • Breathing • Anti Error
# =========================================

import streamlit as st
import edge_tts
import asyncio
import tempfile
import os
import re
import random
import time


# =========================================
# ADAM FIXED CONFIG (BEST SWEET SPOT)
# =========================================

VOICE = "id-ID-ArdiNeural"

RATE = "-9%"      # santai natural
PITCH = "-5Hz"    # deep maskulin
VOLUME = "+0%"


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Adam Voice Indonesia",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Adam Voice Indonesia")
st.caption("Deep • Natural • Podcast • Human-like (Ultra Smooth)")


# =========================================
# HUMANIZER ENGINE (NO MULTI REQUEST)
# =========================================

def humanize_text(text: str):
    """
    Auto jeda + napas manusia TANPA bikin banyak request
    100% stabil untuk edge-tts
    """

    text = re.sub(r"\s+", " ", text.strip())

    # jeda alami
    text = text.replace(",", ", ... ")
    text = text.replace(".", ". ..... ")
    text = text.replace("?", "? ..... ")
    text = text.replace("!", "! ..... ")
    text = text.replace("\n", " ......... ")

    # napas random tiap 12-18 kata
    words = text.split()
    result = []

    for i, w in enumerate(words):
        result.append(w)

        if i > 6 and i % random.randint(12, 18) == 0:
            result.append("...")

    return " ".join(result)


# =========================================
# TTS SINGLE REQUEST (ANTI ERROR)
# =========================================

async def generate(text):

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp.close()

    communicate = edge_tts.Communicate(
        text=text,          # 🔥 kirim SEKALI saja
        voice=VOICE,
        rate=RATE,
        pitch=PITCH,
        volume=VOLUME
    )

    await communicate.save(temp.name)

    return temp.name


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


if st.button("🎙️ Generate Adam Voice", use_container_width=True):

    if not text:
        st.warning("Masukkan teks dulu")
        st.stop()

    with st.spinner("Generating natural voice..."):

        processed_text = humanize_text(text)

        file_path = asyncio.run(generate(processed_text))

        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        st.success("Selesai! Suara natural siap dipakai 🎧")

        st.audio(audio_bytes)

        st.download_button(
            "⬇️ Download MP3",
            audio_bytes,
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
🔥 Adam Ultra Realistic aktif:
✅ Auto jeda manusia
✅ Auto napas
✅ Tidak robotik
✅ 1x request (anti error edge-tts)
✅ Podcast / Narator vibe

Setting tetap:
Voice : Ardi Neural
Rate  : -9%
Pitch : -5Hz
""")
