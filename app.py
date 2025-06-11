import streamlit as st
from gtts import gTTS
import base64
from tempfile import NamedTemporaryFile

# App title
st.title("🗣️ Natural Voices - Text to Speech")

# ---- Sidebar Settings ----
st.sidebar.header("🎛 Settings")

# Extended language list for gTTS
languages = {
    "English (US)": "en",
    "English (UK)": "en-uk",
    "Bangla (Bangladesh)": "bn",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Mandarin Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Turkish": "tr",
    "Tamil": "ta",
    "Urdu": "ur",
    "Italian": "it",
    "Polish": "pl",
    "Dutch": "nl"
}

selected_lang = st.sidebar.selectbox("🌐 Language", list(languages.keys()))
lang_code = languages[selected_lang]

voice_type = st.sidebar.radio("👤 Voice Type", ["Female"])  # gTTS supports only female
speech_speed = st.sidebar.slider("🎚️ Speed (0.5 = Slow, 1 = Normal)", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
volume_level = st.sidebar.slider("🔊 Volume", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

# ---- Text Input ----
st.subheader("✍️ Enter Text Below")
text_input = st.text_area("This app is designed to convert text into natural-sounding speech and developed by Noman",)

# ---- Generate Button ----
if st.button("🔊 Generate Speech"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text to convert.")
    else:
        slow = speech_speed < 0.75  # treat <0.75 as slow
        tts = gTTS(text=text_input, lang=lang_code, slow=slow)

        with NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            audio_path = tmpfile.name

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()

        # Custom HTML audio player with volume control
        audio_html = f"""
        <audio autoplay controls style="width: 100%;" onvolumechange="this.volume={volume_level}">
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.success("✅ Speech generated successfully!")
        st.markdown(audio_html, unsafe_allow_html=True)

        # Download button
        st.download_button("⬇️ Download MP3", audio_bytes, file_name="audio_output.mp3", mime="audio/mp3")
