import subprocess
import shutil

class JarvisAutomation:

    ALLOWED_COMMANDS = {
        "date": ["date"],
        "time": ["date", "+%H:%M:%S"],
        "storage": ["df", "-h"],
        "memory": ["free", "-h"],
        "files": ["ls", "-lah"],
        "internet": ["curl", "-I", "--max-time", "10", "https://example.com"]
    }

    def run_task(self, task):
        if task not in self.ALLOWED_COMMANDS:
            return "Sir, this task is not allowed."

        command = self.ALLOWED_COMMANDS[task]

        if not shutil.which(command[0]):
            return f"{command[0]} command available nahi hai."

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=15
            )

            return result.stdout.strip() or result.stderr.strip()

        except Exception as error:
            return f"Automation error: {error}"


if __name__ == "__main__":
    jarvis = JarvisAutomation()

    print("JARVIS AUTOMATION ENGINE ONLINE")
    print("\nDate:")
    print(jarvis.run_task("date"))

    print("\nStorage:")
    print(jarvis.run_task("storage"))
