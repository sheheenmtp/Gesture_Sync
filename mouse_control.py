import sys
from tkinter import Tk, Canvas, Button, PhotoImage
from pathlib import Path
from threading import Thread
from one_code import start_gesture_control
from vol_control import volume_control, v_deactivate_analysis
from open_control import hand_gesture_analysis, deactivate_analysis

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\mini_project\GUI\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def ter():
    sys.exit()


def start_voice_thread():
    voice_thread = Thread(target=start_gesture_control)
    voice_thread.start()


def start_volume_thread():
    volume_thread = Thread(target=volume_control)
    volume_thread.start()


def start_finger_thread():
    finger_thread = Thread(target=hand_gesture_analysis)
    finger_thread.start()


def deactivate():
    def wrapper():
        deactivate_analysis()
        v_deactivate_analysis()

    de_thread = Thread(target=wrapper)
    de_thread.start()

def close():
    ter()
    ter_thread = Thread(target=ter)
    ter_thread.start()

window = Tk()
window.geometry("700x550")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=550,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load images
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))

# Create buttons
buttons = [
    Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=start_voice_thread, relief="flat"),
    Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=start_volume_thread, relief="flat"),
    Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: print("Button 3 clicked"), relief="flat"),
    Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=start_finger_thread, relief="flat"),
    Button(image=button_image_5, borderwidth=0, highlightthickness=0, command=deactivate, relief="flat"),
    Button(image=button_image_6, borderwidth=0, highlightthickness=0, command=ter, relief="flat")
]

# Place buttons
positions = [(577.0, 0.0), (71.0, 151.0), (270.0, 151.0), (469.0, 151.0), (191.0, 234.0), (400.0, 234.0)]
for button, (x, y) in zip(buttons, positions):
    button.place(x=x, y=y, width=button_image_1.width(), height=button_image_1.height())

window.resizable(False, False)
window.mainloop()
