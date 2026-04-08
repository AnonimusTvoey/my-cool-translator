import keyboard
import pyperclip
import requests
import time
import tkinter as tk
from tkinter import messagebox

# Твой новый ключ
API_KEY = "AIzaSyDcTlUtgeiTD9fAUD26PVK9NDmUGw1kcJg"

# МЕНЯЕМ МОДЕЛЬ НА GEMINI-PRO
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

def ai_request(text, prompt):
    # У Gemini Pro чуть другой формат запроса, подправляем его
    payload = {
        "contents": [{
            "parts": [{"text": f"{prompt}\n\nText: {text}"}]
        }]
    }
    try:
        response = requests.post(URL, json=payload, timeout=20)
        data = response.json()
        
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        elif 'error' in data:
            return f"Google говорит: {data['error'].get('message', 'Ошибка доступа')}"
        else:
            return f"Ответ не распознан. Возможно, стоит включить VPN."
    except Exception as e:
        return f"Ошибка связи: {str(e)}"

def show_info(title, text):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(title, text)
    root.destroy()

last_c_time = 0
translated_text = ""

def on_ctrl_c():
    global last_c_time, translated_text
    now = time.time()
    if now - last_c_time < 0.5:
        source_text = pyperclip.paste()
        if not source_text or len(source_text.strip()) < 1:
            return
            
        prompt = "Translate to casual American English with Gen-Z slang (no cap, fr, bussin). Make it sound natural."
        res = ai_request(source_text, prompt)
        
        if "Google говорит" in res or "Ошибка" in res:
            show_info("Проблема", res)
        else:
            translated_text = res
            show_info("Перевод готов!", f"{translated_text}\n\nНажми Ctrl+R для замены.")
    last_c_time = now

def replace_text():
    if translated_text:
        pyperclip.copy(translated_text)
        keyboard.press_and_release('ctrl+v')

def eng_to_rus():
    source_text = pyperclip.paste()
    if not source_text: return
    res = ai_request(source_text, "Переведи на русский язык, живым языком.")
    show_info("На русском", res)

# Горячие клавиши
keyboard.add_hotkey('ctrl+c', on_ctrl_c)
keyboard.add_hotkey('ctrl+r', replace_text)
keyboard.add_hotkey('alt+z', eng_to_rus)

print("Пробуем запуск через Gemini Pro...")
keyboard.wait()
