import streamlit as st
import os
os.system("pip install deep-translator")

from deep_translator import GoogleTranslator
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip


# ✅ Fix: More reliable translation
def translate_text(text, target_lang): #="ta"):
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print("Translation Error:", e)
        return "Translation Failed"

# 🎤 Convert Tamil text to Speech
def text_to_speech(text,lang, filename="speech.mp3"): #="ta"):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

# 🖼️ Generate Image with Tamil Text
def generate_image(text, filename="output.jpg"):
    img = Image.new("RGB", (1280, 720), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    x_position = (img.width - text_width) // 2
    y_position = (img.height - text_height) // 2
    draw.text((x_position, y_position), text, fill="black", font=font)

    img.save(filename, "JPEG")
    return filename

# 🎥 Create Video from Image and Tamil Audio
def create_video(image_path, audio_path, output_video="output.mp4"):
    image_clip = ImageClip(image_path).set_duration(5)
    audio_clip = AudioFileClip(audio_path)

    image_clip = image_clip.resize(height=720)
    
    final_clip = CompositeVideoClip([image_clip]).set_audio(audio_clip)
    final_clip.write_videofile(output_video, fps=24, codec="libx264")
    return output_video

# 🌐 Streamlit UI
st.title("Welcome to Language Generator Developed by Twinkle Kids Channel")

text_input = st.text_area("Enter your English text:", "Hello, how are you?")
language = st.selectbox(
    "Choose a Language:",
    ["Tamil", "English", "Hindi", "French", "Malay"]
)

if st.button("Generate Tamil Video"):
    st.write("Processing...")
    
    if language =='English':
        language = 'en'
    elif language =='Tamil':  
        language = 'ta'  
    elif language =='Hindi':  
        language = 'hi'  
    elif language =='Malay':  
        language = 'ms'  
    elif language =='French':  
        language = 'fr'
    else:
        st.write('Please enter correct language')     
    tamil_text = translate_text(text_input,language)  # 🔹 Translate English → Tamil
    st.write(f"**Translated Tamil Text:** {tamil_text}")

    #image_file = generate_image(tamil_text)  # 🖼️ Create Image with Tamil Text
    audio_file = text_to_speech(tamil_text,language)  # 🎤 Generate Tamil Speech
    #video_file = create_video( ) #image_file, audio_file)  # 🎥 Create Video
    st.audio(audio_file) 

    #st.video(video_file)
    st.success("Tamil Video Generated Successfully!")
