import keyboard
import pyperclip
import requests
import customtkinter as ctk
import threading
import time

# === НАСТРОЙКИ GROQ ===
GROQ_API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile" # Топовая модель от Meta

class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Groq Ultra-Fast Translator")
        self.geometry("700x450")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text="POWERED BY GROQ (LLAMA 3)", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.input_text = ctk.CTkTextbox(self, width=300, corner_radius=10, fg_color="#2f3136", border_color="#202225")
        self.input_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.input_text.insert("0.0", "Введите текст или нажмите Ctrl+C дважды...")

        self.output_text = ctk.CTkTextbox(self, width=300, corner_radius=10, fg_color="#2f3136", border_color="#202225")
        self.output_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.output_text.insert("0.0", "Здесь появится перевод...")

        self.btn_translate = ctk.CTkButton(self, text="Translate", command=self.manual_translate, fg_color="#5865f2", hover_color="#4752c4")
        self.btn_translate.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Система на Groq готова", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=3, column=0, columnspan=2, padx=20, pady=5)

        self.last_c_time = 0
        self.translated_storage = ""
        self.bind_hotkeys()
        self.check_startup()

    def ai_request(self, text, prompt):
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            "temperature": 0.7
        }
        try:
            response = requests.post(URL, headers=headers, json=payload, timeout=10)
            data = response.json()
            if 'choices' in data:
                return data['choices'][0]['message']['content'].strip()
            return f"Ошибка Groq: {data.get('error', {}).get('message', 'Unknown')}"
        except Exception as e:
            return f"Ошибка сети: {str(e)}"

    def update_ui_text(self, source, target):
        self.input_text.delete("0.0", "end")
        self.input_text.insert("0.0", source)
        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", target)
        self.translated_storage = target

    def manual_translate(self):
        text = self.input_text.get("0.0", "end").strip()
        if not text: return
        self.status_label.configure(text="Groq переводит...", text_color="yellow")
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
                self.status_label.configure(text="Молниеносный перевод...", text_color="#5865f2")
                # Улучшенный промпт для сленга
                prompt = "You are a professional Gen-Z translator. Translate the text to casual American English with modern slang (no cap, fr, vibe, etc.). Be natural."
                res = self.ai_request(source, prompt)
                self.update_ui_text(source, res)
                self.deiconify() 
                self.status_label.configure(text="Переведено мгновенно!", text_color="green")
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
            if "Ошибка" in res:
                self.status_label.configure(text=f"Статус: {res}", text_color="red")
            else:
                self.status_label.configure(text="Groq подключен! Скорость максимальная.", text_color="green")
        threading.Thread(target=task).start()

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
