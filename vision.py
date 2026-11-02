import os
import subprocess

class JarvisVision:

    def read_screen(self, image_path=None):

        if not image_path:
            print("Sir, screenshot ka path dijiye.")
            image_path = input("Image path: ").strip()

        image_path = os.path.expanduser(image_path)

        if not os.path.isfile(image_path):
            return "Screenshot file nahi mili."

        try:
            result = subprocess.run(
                [
                    "tesseract",
                    image_path,
                    "stdout",
                    "-l", "eng"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return result.stderr

            text = result.stdout.strip()

            return text if text else "Screen par text nahi mila."

        except Exception as error:
            return f"Vision error: {error}"


if __name__ == "__main__":
    vision = JarvisVision()
    print(vision.read_screen())
