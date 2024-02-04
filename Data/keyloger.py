from pynput import keyboard
import time

def on_press(key):
    try:
        write_to_file(f'keyboard.Controller().press({key})')
    except AttributeError:
        write_to_file(f'keyboard.Controller().press(\'{key}\')')


def on_release(key):
    try:
        write_to_file(f'keyboard.Controller().release({key})')
    except AttributeError:
        write_to_file(f'keyboard.Controller().release(\'{key}\')')


def write_to_file(message):
    with open('log.txt', 'a') as file:
        file.write(f'{message}\n')


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

    time.sleep(10)

    with open('log.txt') as file:
        lines = file.readlines()

    with open('execute.py', 'w') as file:
        for line in lines:
            file.write(f'{line.strip()}\n')
