import keyboard
import pyperclip
import requests
import time
import tkinter as tk
from tkinter import messagebox

# Твой ключ (советую потом заменить на новый и никому не показывать)
API_KEY = "AIzaSyAtg2QqnG_fr49XTTpvsUp-6yru1XxzElY"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def ai_request(text, prompt):
    payload = {"contents": [{"parts": [{"text": f"{prompt}\n\nText: {text}"}]}]}
    try:
        response = requests.post(URL, json=payload, timeout=10)
        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        return f"Ошибка: {str(e)}"

def show_info(text):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo("Переводчик", text)
    root.destroy()

last_c_time = 0
translated_text = ""

def on_ctrl_c():
    global last_c_time, translated_text
    now = time.time()
    if now - last_c_time < 0.5:
        source_text = pyperclip.paste()
        # Инструкция для живого американского сленга
        prompt = "Translate this to natural, casual American English. Use modern Gen-Z slang (no cap, fr, bussin, etc.) where it fits. Make it sound very alive."
        translated_text = ai_request(source_text, prompt)
        show_info(f"Перевод (Сленг):\n{translated_text}\n\nНажми Ctrl+R для замены текста.")
    last_c_time = now

def replace_text():
    if translated_text:
        pyperclip.copy(translated_text)
        keyboard.press_and_release('ctrl+v')

def eng_to_rus():
    source_text = pyperclip.paste()
    prompt = "Переведи этот текст на русский язык. Пусть звучит естественно и современно."
    res = ai_request(source_text, prompt)
    show_info(f"Перевод на русский:\n{res}")

# Горячие клавиши
keyboard.add_hotkey('ctrl+c', on_ctrl_c)
keyboard.add_hotkey('ctrl+r', replace_text)
keyboard.add_hotkey('alt+z', eng_to_rus) # Alt+Z для перевода с английского на русский

print("Приложение запущено!")
keyboard.wait()
