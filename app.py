import streamlit as st
from PIL import Image
import os
from datetime import datetime

from pipeline.captioner import Captioner
from pipeline.storyteller import StoryTeller
from pipeline.prompts import build_story_prompt

st.set_page_config(page_title="Image → Story Generator", page_icon="🖼️", layout="centered")

@st.cache_resource
def get_captioner():
    return Captioner()

@st.cache_resource
def get_storyteller():
    return StoryTeller()


st.title("🖼️ Image → Story Generator (DL Project)")
st.write("Upload an image → get a caption + a story.")

style = st.selectbox("Choose story style", ["mystery", "motivational", "comedy", "crime"])
word_limit = st.slider("Story length (approx words)", 80, 180, 140, 10)

# Debug mode checkbox
debug_mode = st.checkbox("🔧 Show debug info (rough + final story)", value=False)

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

if uploaded:
    image = Image.open(uploaded)
    if "last_file" not in st.session_state or st.session_state["last_file"] != uploaded.name:
        st.session_state["caption"] = ""
        st.session_state["last_file"] = uploaded.name

    st.image(image, caption="Uploaded image", use_container_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            captioner = get_captioner()
            st.session_state["caption"] = captioner.caption(image)


    caption = st.session_state.get("caption", "")
    if caption:
        st.subheader("Caption")
        st.write(caption)

        if st.button("Generate Story"):
            prompt = build_story_prompt(caption, style, word_limit)
            with st.spinner("Generating story (two-pass generation)..."):
                storyteller = get_storyteller()
                result = storyteller.generate(prompt, debug=debug_mode)

            # Handle both debug and normal mode
            if debug_mode:
                rough, final = result
                st.subheader("Debug: Rough Story (First Pass)")
                st.text_area("Rough Output", rough, height=150, disabled=True)
                st.subheader("Output: Final Story (Expanded)")
                out = final
            else:
                out = result

            st.text_area("Result", out, height=260)

            os.makedirs("outputs", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"outputs/{ts}_{style}.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write("CAPTION:\n" + caption + "\n\nPROMPT:\n" + prompt + "\n\nOUTPUT:\n" + out)
            st.success(f"Saved: {path}")
else:
    st.info("Upload an image to start.")

