import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

# Fonts directory
FONTS_DIR = "fonts"
FONT_OPTIONS = {
    "Impact": os.path.join(FONTS_DIR, "impact.ttf"),
    "Anton": os.path.join(FONTS_DIR, "anton.ttf"),
    "Lobster": os.path.join(FONTS_DIR, "lobster.ttf"),
    "Arial": os.path.join(FONTS_DIR, "arial.ttf"),
}

# Centered text drawing
def draw_text(draw, text, font, image_width, y_position):
    text_width, _ = draw.textsize(text, font=font)
    x_position = (image_width - text_width) // 2
    draw.text((x_position, y_position), text, font=font, fill="white", stroke_width=2, stroke_fill="black")

# Meme generator
def create_meme(image, top_text, bottom_text, font_path):
    image = image.convert("RGB")
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    font_size = int(image_height * 0.08)

    font = ImageFont.truetype(font_path, font_size)

    # Draw top text
    draw_text(draw, top_text.upper(), font, image_width, 10)

    # Draw bottom text
    text_height = draw.textsize(bottom_text, font=font)[1]
    draw_text(draw, bottom_text.upper(), font, image_width, image_height - text_height - 10)

    return image

# UI
st.title("🖼️ Meme Generator")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
top_text = st.text_input("Top Text")
bottom_text = st.text_input("Bottom Text")
font_choice = st.selectbox("Choose Font", list(FONT_OPTIONS.keys()))

if uploaded_file:
    image = Image.open(uploaded_file)
    font_path = FONT_OPTIONS[font_choice]

    if st.button("Generate Meme"):
        meme = create_meme(image, top_text, bottom_text, font_path)
        st.image(meme, caption="Generated Meme", use_column_width=True)

        # Save and offer download
        meme.save("meme_output.jpg")
        with open("meme_output.jpg", "rb") as f:
            st.download_button("Download Meme", f, file_name="your_meme.jpg", mime="image/jpeg")
