# 🖼️ Image to Story Generator (Deep Learning Project)

A multimodal deep learning application that converts an image into a descriptive caption and then generates a short story in different styles such as **Mystery, Motivational, Comedy, and Crime**.

This project demonstrates how pretrained vision-language and text-generation models can be integrated into a single pipeline and deployed using a simple web interface.

---

## 🚀 Features
- Image captioning using a pretrained vision-language model
- Story generation using a pretrained transformer-based language model
- Multiple storytelling styles:
  - Mystery
  - Motivational
  - Comedy
  - Crime
- CPU-only (no GPU required)
- Lightweight and beginner-friendly
- Interactive Streamlit web interface

---

## 🧠 Models Used
- **Image Captioning:** BLIP (Salesforce BLIP Image Captioning)
- **Story Generation:** Google FLAN-T5 (instruction-tuned text generation model)

All models are loaded from **Hugging Face** and used without additional training.

---

## 🛠️ Tech Stack
- Python 3.11
- PyTorch
- Hugging Face Transformers
- Streamlit
- Pillow (image processing)

---

## ⚙️ How It Works
1. User uploads an image
2. The image is passed to an image-captioning model
3. The generated caption is converted into a structured prompt
4. A story is generated based on the selected style
5. The final output is displayed and saved locally

---

## ▶️ How to Run the Application (Local Setup)

### 1️⃣ Install dependencies
```bash
pip install streamlit transformers pillow torch
