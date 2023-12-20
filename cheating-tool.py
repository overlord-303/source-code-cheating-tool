import tkinter as tk
from datetime import datetime
import openai
import time
import sys
import keyboard


class ClipboardMonitor:
    def __init__(self, interval=1000, cooldown_duration=10,
                 openai_api_key="HIDDEN_FOR_PRIV"):
        self.root = tk.Tk()
        self.root.withdraw()
        self.last_clipboard_content = self.get_clipboard_content()
        self.interval = interval
        self.cooldown_duration = cooldown_duration
        self.last_response_time = 0
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.monitor_clipboard()

    def get_clipboard_content(self):
        try:
            return self.root.clipboard_get()
        except tk.TclError:
            return 'Clipboard was empty.'

    def set_clipboard_content(self, content):
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()

    def writeFile(self, status):
        now = datetime.now()
        date_time = now.strftime("%m.%d.%y - %H:%M:%S")
        final_time = f"[{date_time}] "
        with open("log.txt", "a") as f:
            f.write(f"{final_time}\n{status}\n")

    def end_program(self):
        print("Program terminated by user.")
        self.set_clipboard_content('Placeholder')
        sys.exit(0)

    def monitor_clipboard(self):

        current_clipboard_content = self.get_clipboard_content()
        current_time = time.time()

        if keyboard.is_pressed('ctrl+ctrl'):
            self.end_program()

        if current_clipboard_content.lower() == "end":
            self.end_program()

        if current_clipboard_content != self.last_clipboard_content and (
                current_time - self.last_response_time) > self.cooldown_duration:
            responseInput = "Clipboard content changed: \n" + current_clipboard_content
            print(responseInput)

            response = self.generate_response(current_clipboard_content)
            responseOutput = "OpenAI GPT Response: \n" + response
            print(responseOutput)

            logText = responseInput + "\n" + responseOutput + "\n"
            self.writeFile(logText)

            self.set_clipboard_content(response)

            self.last_response_time = current_time

        self.last_clipboard_content = current_clipboard_content
        self.root.after(self.interval, self.monitor_clipboard)

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Answer the question short and simple but to the best of your knowledge, max. 1 sentence. Language depends on user input."},
                {"role": "user", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content'].strip()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    clipboard_monitor = ClipboardMonitor(openai_api_key="HIDDEN_FOR_PRIV")
    clipboard_monitor.run()

