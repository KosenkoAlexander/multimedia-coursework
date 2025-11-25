import tkinter as tk
from tkinter import Canvas
import pygame
from PIL import Image, ImageTk

from text_and_speech.tts import TTS

# https://kamil.myblog.arts.ac.uk/2021/01/04/phonemes/
class PhonemeVisualizer:
    
    def __init__(self, root, wav_path):
        self.root = root

        self.canvas = Canvas(root, width=500, height=300, bg="white")
        self.canvas.pack()
        self.canvas.create_image(150,50, anchor=tk.NW, image=None, tags="mouth")
        self.text_id = self.canvas.create_text(250, 200, font=("Arial", 24), tag="text")
        self.phoneme_image: Image.Image = None

        pygame.mixer.init()
        pygame.mixer.music.load(wav_path)

        tk.Button(root, command=self._run).pack()


    def _run(self):
        pygame.mixer.music.play()
        self.update_loop(0)


    def draw_phoneme(self, ph):
        """Draw a shape for the given phoneme."""
        # self.canvas.delete("all")
        group = self.get_phoneme_group(ph)
        # numbers that depend on reference image
        w = 124
        h = 130
        x = (group-1)%5 * w
        y = 0 if group <= 5 else 155

        self.phoneme_image = ImageTk.PhotoImage(image.crop((x,y,x+w,y+h)))
        self.canvas.itemconfig("mouth", image=self.phoneme_image)
        self.canvas.itemconfig("text", text=ph)


    @staticmethod
    def get_phoneme_group(ph: str):
        if ph.startswith("AO") or ph.startswith("UH") or ph.startswith("O"):
            return 2  # O
        elif ph.startswith("A") or ph.startswith("I"):
            return 1  # AI
        elif ph.startswith("E"):
            return 6  # E
        elif ph.startswith("UW"):
            return 7  # U
        elif ph in ["F", "V"]:
            return 8  # V
        elif ph in ["M", "B", "P"]:
            return 9  # B
        elif ph in ["W", "Q"]:
            return 5  # Q
        elif ph == "L":
            return 4  # L
        elif ph[0].isalpha():
            return 3  # pointy consonant
        else:
            return 10 # rest


    def update_loop(self, phoneme_index: int):
        """Update visuals phoneme-by-phoneme parallel to the audio"""
        print(pygame.mixer.music.get_pos())
        if phoneme_index >= len(phonemes):
            return
        current = phonemes[phoneme_index]
        self.draw_phoneme(current["phoneme"])

        self.root.after(current["delay"], self.update_loop, phoneme_index+1)



tts = TTS()
out_path, phonemes = tts.run("""Hello world. Nice one, and nice another. Look at me go, i am unstoppable.""")
image = Image.open("phoneme_mouth_chart.jpg")


def main():
    root = tk.Tk()
    root.title("Phoneme Visualizer")
    app = PhonemeVisualizer(root, "tmp/response.wav")
    root.mainloop()


if __name__ == "__main__":
    main()
