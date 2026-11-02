import json
from pathlib import Path
from datetime import datetime

class JarvisMemory:

    def __init__(self):
        self.file = Path.home() / "JARVIS" / "data" / "memory.json"
        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.save([])

    def save(self, data):
        self.file.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def remember(self, role, message):
        data = self.recall()

        data.append({
            "role": role,
            "message": message,
            "time": datetime.now().isoformat()
        })

        self.save(data)
        return "Memory saved successfully."

    def recall(self):
        try:
            return json.loads(
                self.file.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return []

    def clear(self):
        self.save([])
        return "Memory cleared."


if __name__ == "__main__":
    jarvis = JarvisMemory()

    print("JARVIS MEMORY ENGINE ONLINE")
    print(jarvis.remember("user", "Hello JARVIS"))
    print("Saved memories:", len(jarvis.recall()))
