import keyboard
import pyperclip
import requests
import time
import tkinter as tk
from tkinter import messagebox

# Вставь сюда свой НОВЫЙ ключ
API_KEY = "AIzaSyDcTlUtgeiTD9fAUD26PVK9NDmUGw1kcJg"

# Пробуем достучаться через универсальный путь
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

def ai_request(text, prompt):
    payload = {
        "contents": [{
            "parts": [{"text": f"{prompt}\n\nText: {text}"}]
        }]
    }
    try:
        response = requests.post(URL, json=payload, timeout=15)
        data = response.json()
        
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        elif 'error' in data:
            # Если не находит модель, попробуем сказать пользователю, что делать
            msg = data['error'].get('message', '')
            if "not found" in msg.lower():
                return "Ошибка: Модель не найдена. Попробуй зайти в AI Studio и проверить доступность Gemini 1.5 Flash."
            return f"Google говорит: {msg}"
        else:
            return f"Формат ответа не распознан: {str(data)}"
    except Exception as e:
        return f"Ошибка сети: {str(e)}"

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
            
        prompt = "Translate to casual American English with Gen-Z slang. Use words like 'no cap', 'fr', 'bet'. Make it sound like a native teen."
        res = ai_request(source_text, prompt)
        
        if "Ошибка" in res or "Google говорит" in res:
            show_info("Проблема", res)
        else:
            translated_text = res
            show_info("Перевод готов!", f"{translated_text}\n\nНажми Ctrl+R для замены текста.")
    last_c_time = now

def replace_text():
    if translated_text:
        pyperclip.copy(translated_text)
        keyboard.press_and_release('ctrl+v')

def eng_to_rus():
    source_text = pyperclip.paste()
    if not source_text: return
    res = ai_request(source_text, "Переведи на русский язык, живым и естественным языком.")
    show_info("На русском", res)

# Горячие клавиши
keyboard.add_hotkey('ctrl+c', on_ctrl_c)
keyboard.add_hotkey('ctrl+r', replace_text)
keyboard.add_hotkey('alt+z', eng_to_rus)

print("Программа запущена. Пробуй!")
keyboard.wait()
