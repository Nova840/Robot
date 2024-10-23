from pynput import keyboard, mouse
from time import sleep

def on_press(key):
    keyStr = str(key).upper()
    if keyStr == "','":
        print("\nPressed: KEY_'COMMA'")
    elif keyStr == "KEY.ESC":
        print("Escape is used to terminate the program, so you're not allowed to use escape as input.")
    else
        print("\nPressed: KEY_" + keyStr)

def on_click(x, y, button, pressed):
    if pressed:
        print("\nPressed: KEY_" + str(button))

def main():
    print("Press any key to see value. Press CTRL + C to exit.")

    k_listener  = keyboard.Listener(on_press = on_press, suppress = False)
    k_listener.start()

    m_listener = mouse.Listener(on_click = on_click, suppress = False)
    m_listener.start()

    while True:
        sleep(1)

if __name__ == "__main__":
    main()