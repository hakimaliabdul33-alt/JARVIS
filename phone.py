import subprocess
import shutil

class JarvisPhone:

    def run_command(self, command):
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
            return f"Phone error: {error}"

    def battery(self):
        return self.run_command(["termux-battery-status"])

    def device_info(self):
        return self.run_command(["getprop", "ro.product.model"])

    def wifi_info(self):
        return self.run_command(["termux-wifi-connectioninfo"])


if __name__ == "__main__":
    jarvis = JarvisPhone()

    print("JARVIS PHONE CONTROL ONLINE")
    print("Device:", jarvis.device_info())
    print("Battery:", jarvis.battery())
