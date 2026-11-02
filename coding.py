import os
from pathlib import Path

class JarvisCoder:

    def __init__(self):
        self.workspace = Path.home() / "JARVIS" / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)

    def create_file(self, filename, code):
        path = Path(filename)

        if path.name != filename or filename in ("", ".", ".."):
            return "Invalid filename."

        allowed = {
            ".py", ".java", ".kt", ".js",
            ".html", ".css", ".json", ".txt",
            ".sh", ".cpp", ".c"
        }

        if path.suffix.lower() not in allowed:
            return "File extension not allowed."

        target = self.workspace / filename

        if target.exists():
            return "File already exists. Not overwritten."

        target.write_text(code, encoding="utf-8")
        return f"Sir, file created: {target}"

    def read_file(self, filename):
        path = Path(filename)

        if path.name != filename:
            return "Invalid filename."

        target = self.workspace / filename

        if not target.is_file():
            return "File not found."

        return target.read_text(encoding="utf-8")

    def list_files(self):
        return [
            p.name for p in self.workspace.iterdir()
            if p.is_file()
        ]


if __name__ == "__main__":
    coder = JarvisCoder()
    print("JARVIS CODING ENGINE ONLINE")
    print("Workspace:", coder.workspace)
    print("Files:", coder.list_files())
