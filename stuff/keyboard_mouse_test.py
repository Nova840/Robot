from pynput.keyboard import Key, Listener as KListener
from pynput.mouse import Button, Listener as MListener
import _thread

print("Press any key to see value. Press CTRL + C to exit.")

def on_press(key):
    keyStr = str(key).upper()
    print("\nPressed: " + keyStr)
    if keyStr == "','":
        print("Comma is used to separate values in input.txt, so you're not allowed to use a comma as input.")
    elif keyStr == "KEY.ESC":
        print("Escape is used to terminate the program, so you're not allowed to use escape as input.")

def on_release(key):
    return

def k_listen():
    with KListener(on_press = on_press, on_release = on_release) as k_listener:
        k_listener.join()

def on_click(x, y, button, pressed):
    if not pressed:
        return
    print("\nPressed: " + str(button))

def m_listen():
    with MListener(on_click = on_click) as m_listener:
        m_listener.join()

_thread.start_new_thread(k_listen, ())
_thread.start_new_thread(m_listen, ())

while True:
    pass