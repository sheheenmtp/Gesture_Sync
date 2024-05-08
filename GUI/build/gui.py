import sys
import sys
from tkinter import Tk, Canvas, Button, PhotoImage
from pathlib import Path
from threading import Thread
from one_code import start_gesture_control
from vol_control import volume_control,  v_deactivate_analysis
from open_control import hand_gesture_analysis, deactivate_analysis


def ter():
    sys.exit()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\mini_project\GUI\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def start_voice_thread():
    voice_thread = Thread(target=start_gesture_control)
    voice_thread.start()


def start_volume_thread():
    volume_thread = Thread(target=volume_control)
    volume_thread.start()


def start_finger_thread():
    finger_thread = Thread(target=hand_gesture_analysis)
    finger_thread.start()


def deactivate_and_close():
    def wrapper():
        deactivate_analysis()
        v_deactivate_analysis()

    de_thread = Thread(target=wrapper)
    de_thread.start()


window = Tk()

window.geometry("700x550")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 550,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    275.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    350.0,
    427.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    350.0,
    30.0,
    image=image_image_3
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_voice_thread,
    relief="flat"
)
button_1.place(
    x=577.0,
    y=0.0,
    width=123.0,
    height=61.0
)

canvas.create_text(
    15.0,
    83.0,
    anchor="nw",
    text="manual control",
    fill="#3E2929",
    font=("Kollektif", 28 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=start_volume_thread,
    relief="flat"
)
button_2.place(
    x=71.0,
    y=151.0,
    width=161.0,
    height=46.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_3.place(
    x=270.0,
    y=151.0,
    width=163.0,
    height=46.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=start_finger_thread,
    relief="flat"
)
button_4.place(
    x=469.0,
    y=151.0,
    width=161.0,
    height=46.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=deactivate_and_close,
    relief="flat"
)
button_5.place(
    x=191.0,
    y=234.0,
    width=115.0,
    height=33.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=ter,
    relief="flat"
)
button_6.place(
    x=400.0,
    y=234.0,
    width=115.0,
    height=33.0
)
window.resizable(False, False)
window.mainloop()

