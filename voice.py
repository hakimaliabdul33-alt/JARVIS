import subprocess
import shutil

class JarvisVoice:

    def speak(self, text):
        if shutil.which("espeak"):
            subprocess.run(
                ["espeak", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )

    def listen(self):
        try:
            return input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            return "exit"


if __name__ == "__main__":
    jarvis = JarvisVoice()
    jarvis.speak("Hello Sir. Jarvis is online.")
    print("You entered:", jarvis.listen())
