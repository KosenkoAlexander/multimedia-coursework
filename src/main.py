# full program should be started from here
import tkinter as tk
from pygame import mixer

if __name__=='__main__':
    mixer.init()
    sound = mixer.Sound("tmp/response.wav")

    root = tk.Tk()
    tk.Button(root, command=sound.play).pack()
    root.mainloop()
