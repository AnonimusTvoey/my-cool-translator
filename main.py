import keyboard
import pyperclip
import requests
import time
import tkinter as tk
from tkinter import messagebox

# Твой ключ (если этот не работает, создай НОВЫЙ в AI Studio)
API_KEY = "AIzaSyAtg2QqnG_fr49XTTpvsUp-6yru1XxzElY"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def ai_request(text, prompt):
    payload = {"contents": [{"parts": [{"text": f"{prompt}\n\nText: {text}"}]}]}
    try:
        response = requests.post(URL, json=payload, timeout=10)
        data = response.json()
        
        # Проверяем, есть ли ответ от ИИ
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        elif 'error' in data:
            # Если Google прислал ошибку, выводим её текст
            return f"Ошибка Google API: {data['error'].get('message', 'Неизвестная ошибка')}"
        else:
            return f"Непонятный ответ от сервера: {str(data)}"
    except Exception as e:
        return f"Ошибка соединения: {str(e)}"

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
        if not source_text.strip():
            return
            
        prompt = "Translate this to natural, casual American English. Use modern Gen-Z slang. Make it sound very alive."
        res = ai_request(source_text, prompt)
        
        if "Ошибка" in res:
            show_info("Упс!", res)
            translated_text = ""
        else:
            translated_text = res
            show_info("Готово!", f"Перевод:\n{translated_text}\n\nНажми Ctrl+R для замены.")
    last_c_time = now

def replace_text():
    if translated_text:
        pyperclip.copy(translated_text)
        keyboard.press_and_release('ctrl+v')

def eng_to_rus():
    source_text = pyperclip.paste()
    if not source_text.strip(): return
    res = ai_request(source_text, "Переведи на русский язык, живым языком.")
    show_info("Перевод на русский", res)

# Горячие клавиши
keyboard.add_hotkey('ctrl+c', on_ctrl_c)
keyboard.add_hotkey('ctrl+r', replace_text)
keyboard.add_hotkey('alt+z', eng_to_rus)

print("Программа запущена и ждет нажатий...")
keyboard.wait()
