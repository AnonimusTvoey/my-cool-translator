import keyboard
import pyperclip
import requests
import customtkinter as ctk
import threading
import time

# === НАСТРОЙКИ ===
API_KEY = "ВСТАВЬ_СВОЙ_КЛЮЧ"
MODEL_NAME = "gemini-3.1-pro-preview" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка окна в стиле Discord
        self.title("Gemini AI Translator")
        self.geometry("700x450")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue") # Похоже на акцентный цвет Discord

        # Сетка
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Заголовок
        self.label = ctk.CTkLabel(self, text="GEMINI TRANSLATOR", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # Левое поле (Оригинал)
        self.input_text = ctk.CTkTextbox(self, width=300, corner_radius=10, fg_color="#2f3136", border_color="#202225")
        self.input_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.input_text.insert("0.0", "Введите текст или нажмите Ctrl+C дважды...")

        # Правое поле (Перевод)
        self.output_text = ctk.CTkTextbox(self, width=300, corner_radius=10, fg_color="#2f3136", border_color="#202225")
        self.output_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.output_text.insert("0.0", "Здесь появится перевод...")

        # Кнопка перевода
        self.btn_translate = ctk.CTkButton(self, text="Translate", command=self.manual_translate, fg_color="#5865f2", hover_color="#4752c4")
        self.btn_translate.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        # Статус-бар
        self.status_label = ctk.CTkLabel(self, text="Система готова", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=3, column=0, columnspan=2, padx=20, pady=5)

        # Фоновые процессы
        self.last_c_time = 0
        self.translated_storage = ""
        self.bind_hotkeys()
        self.check_startup()

    def ai_request(self, text, prompt):
        payload = {"contents": [{"parts": [{"text": f"{prompt}\n\nText: {text}"}]}]}
        try:
            response = requests.post(URL, json=payload, timeout=15)
            data = response.json()
            if 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text'].strip()
            return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
        except Exception as e:
            return f"Connection Error: {str(e)}"

    def update_ui_text(self, source, target):
        self.input_text.delete("0.0", "end")
        self.input_text.insert("0.0", source)
        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", target)
        self.translated_storage = target

    def manual_translate(self):
        text = self.input_text.get("0.0", "end").strip()
        self.status_label.configure(text="Перевожу...", text_color="yellow")
        def task():
            res = self.ai_request(text, "Translate to natural English.")
            self.update_ui_text(text, res)
            self.status_label.configure(text="Готово", text_color="green")
        threading.Thread(target=task).start()

    def bind_hotkeys(self):
        def on_ctrl_c():
            now = time.time()
            if now - self.last_c_time < 0.5:
                source = pyperclip.paste()
                self.status_label.configure(text="ИИ думает...", text_color="#5865f2")
                res = self.ai_request(source, "Translate to casual American English with Gen-Z slang.")
                self.update_ui_text(source, res)
                self.deiconify() # Показать окно
                self.status_label.configure(text="Перевод выполнен!", text_color="green")
            self.last_c_time = now

        def on_ctrl_r():
            if self.translated_storage:
                pyperclip.copy(self.translated_storage)
                keyboard.press_and_release('ctrl+v')

        keyboard.add_hotkey('ctrl+c', on_ctrl_c)
        keyboard.add_hotkey('ctrl+r', on_ctrl_r)

    def check_startup(self):
        def task():
            res = self.ai_request("Hi", "Translate to Russian")
            if "Error" in res:
                self.status_label.configure(text=f"ОШИБКА СВЯЗИ: {res}", text_color="red")
            else:
                self.status_label.configure(text="Связь с Gemini установлена (Discord Edition)", text_color="green")
        threading.Thread(target=task).start()

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
