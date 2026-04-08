import keyboard
import pyperclip
import requests
import time
import tkinter as tk
from tkinter import messagebox

# ВНИМАНИЕ: Если этот ключ не работает, создай НОВЫЙ в Google AI Studio.
# Тот, что ты скинул в чат, мог быть заблокирован системой безопасности Google.
API_KEY = "AIzaSyAtg2QqnG_fr49XTTpvsUp-6yru1XxzElY"

# Обновленный URL (используем стабильную версию v1)
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def ai_request(text, prompt):
    payload = {
        "contents": [{
            "parts": [{"text": f"{prompt}\n\nText: {text}"}]
        }]
    }
    try:
        response = requests.post(URL, json=payload, timeout=10)
        data = response.json()
        
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        elif 'error' in data:
            return f"Ошибка Google API: {data['error'].get('message', 'Неизвестная ошибка')}"
        else:
            return f"Неизвестный формат ответа: {str(data)}"
    except Exception as e:
        return f"Ошибка соединения: {str(e)}"

def show_info(title, text):
    root = tk.Tk()
    root.withdraw()
    # Окно всегда будет поверх всех окон
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
            
        # Промпт для молодежного сленга
        prompt = "Translate this to natural, casual American English. Use modern Gen-Z slang (no cap, fr, vibe, etc.). Make it sound like a native teen."
        res = ai_request(source_text, prompt)
        
        if "Ошибка" in res:
            show_info("Проблема с API", res)
            translated_text = ""
        else:
            translated_text = res
            show_info("Перевод (Сленг)", f"{translated_text}\n\n(Нажми Ctrl+R для замены)")
    last_c_time = now

def replace_text():
    if translated_text:
        pyperclip.copy(translated_text)
        keyboard.press_and_release('ctrl+v')

def eng_to_rus():
    source_text = pyperclip.paste()
    if not source_text.strip(): return
    res = ai_request(source_text, "Переведи на русский язык, живым и естественным языком.")
    show_info("На русском", res)

# Горячие клавиши
keyboard.add_hotkey('ctrl+c', on_ctrl_c)
keyboard.add_hotkey('ctrl+r', replace_text)
keyboard.add_hotkey('alt+z', eng_to_rus)

print("Программа запущена! Дважды нажми Ctrl+C для перевода.")
keyboard.wait()
