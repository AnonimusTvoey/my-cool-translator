import keyboard
import pyperclip
import requests
import time
import tkinter as tk
from tkinter import messagebox

# Если ты уже создал НОВЫЙ ключ, вставь его сюда. 
# Если нет — попробуй пока со старым, но ошибка может смениться на "Invalid Key".
API_KEY = "AIzaSyDcTlUtgeiTD9fAUD26PVK9NDmUGw1kcJg"

# МЕНЯЕМ URL на более гибкий формат v1beta (он лучше находит новые модели)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def ai_request(text, prompt):
    # Упаковываем запрос правильно
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
            # Выводим подробности, если это ошибка ключа или лимита
            return f"Google говорит: {data['error'].get('message', 'Неизвестная ошибка')}"
        else:
            return f"Странный ответ: {str(data)}"
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
            
        prompt = "Translate to casual American English with Gen-Z slang. No cap, make it sound natural for a young person."
        res = ai_request(source_text, prompt)
        
        if "Google говорит" in res or "Ошибка" in res:
            show_info("Упс, что-то не так", res)
        else:
            translated_text = res
            show_info("Твой перевод", f"{translated_text}\n\nНажми Ctrl+R для замены текста.")
    last_c_time = now

def replace_text():
    if translated_text:
        pyperclip.copy(translated_text)
        keyboard.press_and_release('ctrl+v')

def eng_to_rus():
    source_text = pyperclip.paste()
    if not source_text: return
    res = ai_request(source_text, "Переведи на русский язык, живым языком.")
    show_info("Перевод на русский", res)

# Горячие клавиши
keyboard.add_hotkey('ctrl+c', on_ctrl_c)
keyboard.add_hotkey('ctrl+r', replace_text)
keyboard.add_hotkey('alt+z', eng_to_rus)

print("Программа обновлена и запущена!")
keyboard.wait()
