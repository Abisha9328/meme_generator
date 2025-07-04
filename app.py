import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Centered text drawing
def draw_text(draw, text, font, image_width, y_position):
    # Get bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x_position = (image_width - text_width) // 2
    draw.text(
        (x_position, y_position),
        text,
        font=font,
        fill="white",
        stroke_width=2,
        stroke_fill="black",
    )

# Meme generator
def create_meme(image, top_text, bottom_text):
    image = image.convert("RGB")
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    # Use default font size proportional to image height
    font_size = int(image_height * 0.08)

    try:
        # Try to load a default truetype font
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        # Fallback to default bitmap font if DejaVu is not available
        font = ImageFont.load_default()

    # Draw top text
    draw_text(draw, top_text.upper(), font, image_width, 10)

    # Get bottom text height
    bbox = draw.textbbox((0, 0), bottom_text, font=font)
    text_height = bbox[3] - bbox[1]
    draw_text(draw, bottom_text.upper(), font, image_width, image_height - text_height - 10)

    return image

# Streamlit UI
st.title("🖼️ Meme Generator")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
top_text = st.text_input("Top Text")
bottom_text = st.text_input("Bottom Text")

if uploaded_file:
    image = Image.open(uploaded_file)

    if st.button("Generate Meme"):
        meme = create_meme(image, top_text, bottom_text)
        st.image(meme, caption="Generated Meme", use_column_width=True)

        # Save and offer download
        meme.save("meme_output.jpg")
        with open("meme_output.jpg", "rb") as f:
            st.download_button("Download Meme", f, file_name="your_meme.jpg", mime="image/jpeg")
else:
    st.info("Upload an image to get started.")
