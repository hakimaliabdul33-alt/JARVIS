from brain import JarvisBrain
from voice import JarvisVoice
from vision import JarvisVision
from coding import JarvisCoder
from phone import JarvisPhone
from automation import JarvisAutomation
from memory import JarvisMemory


class JARVIS:

    def __init__(self):
        self.brain = JarvisBrain()
        self.voice = JarvisVoice()
        self.vision = JarvisVision()
        self.coder = JarvisCoder()
        self.phone = JarvisPhone()
        self.automation = JarvisAutomation()
        self.memory = JarvisMemory()

    def reply(self, message):
        print("\nJARVIS:", message)
        self.voice.speak(message)
        self.memory.remember("assistant", message)

    def help(self):
        return """
JARVIS COMMANDS:

help       - Show commands
battery    - Battery status
device     - Phone model
wifi       - WiFi information
date       - Current date
time       - Current time
storage    - Storage information
files      - Workspace files
screen     - Read screenshot text
code       - Create a code file
memories   - Read saved memories
ask        - Ask AI
exit       - Close JARVIS
"""

    def run(self):
        self.reply("Hello Sir. JARVIS system online.")
        print(self.help())

        while True:
            try:
                command = self.voice.listen().strip()
                task = command.lower()

                if not command:
                    continue

                self.memory.remember("user", command)

                if task == "exit":
                    self.reply("Goodbye Sir.")
                    break

                elif task == "help":
                    self.reply(self.help())

                elif task == "battery":
                    self.reply(self.phone.battery())

                elif task == "device":
                    self.reply(self.phone.device_info())

                elif task == "wifi":
                    self.reply(self.phone.wifi_info())

                elif task in ("date", "time", "storage", "files", "internet"):
                    self.reply(self.automation.run_task(task))

                elif task == "screen":
                    path = input("Screenshot path: ").strip()
                    self.reply(self.vision.read_screen(path))

                elif task == "memories":
                    saved = self.memory.recall()
                    self.reply(f"Total saved memories: {len(saved)}")

                elif task == "code":
                    filename = input("Filename: ").strip()
                    print("Code likhiye. Complete hone par END likhein.")

                    lines = []
                    while True:
                        line = input()
                        if line == "END":
                            break
                        lines.append(line)

                    result = self.coder.create_file(
                        filename,
                        "\n".join(lines)
                    )
                    self.reply(result)

                else:
                    answer = self.brain.ask(command)
                    self.reply(answer)

            except KeyboardInterrupt:
                print("\nJARVIS stopped.")
                break

            except Exception as error:
                self.reply(f"System error: {error}")


if __name__ == "__main__":
    jarvis = JARVIS()
    jarvis.run()
