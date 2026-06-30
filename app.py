import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import os

st.set_page_config(page_title="本地 Whisper 录音转文字", page_icon="🎙️")

st.title("🎙️ 本地 Whisper 录音转文字")
st.caption("所有音频均在本地处理，无需联网，保护隐私")

# Sidebar config
model_size = st.sidebar.selectbox(
    "模型大小（越大越准，但更慢）",
    ["tiny", "base", "small", "medium", "large-v3"],
    index=2,
)
language = st.sidebar.text_input("语言代码（留空自动检测）", value="zh")
st.sidebar.markdown("---")
st.sidebar.markdown("常见语言代码：`zh` 中文, `en` 英语, `ja` 日语")


@st.cache_resource
def load_model(size: str):
    return WhisperModel(size, device="auto", compute_type="default")


model = load_model(model_size)

# Input
audio_value = st.audio_input("点击开始录音（或上传音频文件）")

if audio_value:
    st.audio(audio_value)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_value.getbuffer())
        tmp_path = f.name

    try:
        lang = language if language.strip() else None
        with st.spinner("正在转录，请稍候..."):
            segments, info = model.transcribe(tmp_path, language=lang)
            text = "".join(seg.text for seg in segments)

        st.success(f"转录完成！检测到语言: {info.language}")
        st.write(text)
    finally:
        os.unlink(tmp_path)
