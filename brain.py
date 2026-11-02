import os
from google import genai
from google.genai import types

class JarvisBrain:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.client = None
        self.chat = None

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self.chat = self.client.chats.create(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are JARVIS, an intelligent AI assistant. "
                        "Reply naturally in Hindi or Hinglish when appropriate. "
                        "Help with programming, Android, Termux, Linux, "
                        "science and general questions. Give safe and accurate answers."
                    )
                )
            )

    def ask(self, question):
        if not self.api_key:
            return "Sir, Gemini API key configure nahi hui hai."

        try:
            response = self.chat.send_message(question)
            return response.text or "Sir, Gemini se empty response mila."

        except Exception as error:
            return f"Gemini AI error: {error}"


if __name__ == "__main__":
    jarvis = JarvisBrain()
    print("JARVIS Gemini Brain initialized.")
    print(jarvis.ask("Hindi mein apna parichay dijiye."))
