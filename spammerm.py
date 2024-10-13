# hitem
#!/usr/bin/env python3
import os
import json
from pynput import keyboard, mouse
import threading
import signal
import sys
import time
import colorama
from colorama import Fore, Style
from termcolor import colored

def print_rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    for i, line in enumerate(text.split('\n')):
        print(colored(line, colors[i % len(colors)]))

ascii_art = """
▒█▀▀▀█░▄▀▀▄░█▀▀▄░█▀▄▀█▒█▀▄▀█░█▀▀▄░▀█▀░█▀▀
░▀▀▀▄▄░█▄▄█░█▄▄█░█░▀░█▒█▒█▒█░█▄▄█░░█░░█▀▀
▒█▄▄▄█░█░░░░▀░░▀░▀░░▒▀▒█░░▒█░▀░░▀░░▀░░▀▀▀
"""
print_rainbow_text(ascii_art)
print(Fore.LIGHTMAGENTA_EX + "  [" + Fore.RED + "F5" + Fore.LIGHTMAGENTA_EX + "] Replay   [" + Fore.RED + "F6" + Fore.LIGHTMAGENTA_EX + "] Record   [" + Fore.RED + "F7" + Fore.LIGHTMAGENTA_EX + "] Exit   " + Fore.RESET)
print("")
print(Fore.YELLOW + "→ by hitem                              🖰" + Fore.RESET)
print("------------------------------------------")

class MouseSpammer:
    def __init__(self):
        self.running = False
        self.capturing = False
        self.listener_keyboard = keyboard.Listener(on_press=self.on_press)
        self.listener_mouse = mouse.Listener(on_click=self.on_click)
        self.click_event = None
        self.stop_event = threading.Event()  # Initialize stop_event here
        self.thread = None  # Initialize thread here

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        print(Fore.RED + "Mouse Spamming: OFF" + Style.RESET_ALL)
        self.listener_keyboard.start()
        self.listener_mouse.start()
        self.listener_keyboard.join()
        self.listener_mouse.join()

    def on_press(self, key):
        try:
            if key == keyboard.Key.f5:
                if self.running:
                    self.stop_spamming()
                else:
                    self.start_spamming()
            elif key == keyboard.Key.f6:
                self.toggle_capture()
            elif key == keyboard.Key.f7:
                self.signal_handler(None, None)
        except AttributeError:
            pass

    def on_click(self, x, y, button, pressed):
        if self.capturing and pressed and button == mouse.Button.left:
            self.click_event = (x, y, button)
            print(Fore.BLUE + f"Mouse Click Captured at ({x}, {y})" + Style.RESET_ALL)

    def toggle_capture(self):
        self.capturing = not self.capturing
        if self.capturing:
            print(Fore.CYAN + "Capture Mode: ON" + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "Capture Mode: OFF" + Style.RESET_ALL)

    def start_spamming(self):
        if not self.click_event:
            print(Fore.YELLOW + "No mouse click captured yet!" + Style.RESET_ALL)
            return
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.spam_mouse)
        self.thread.start()
        print(Fore.GREEN + "Mouse Spamming: ON" + Style.RESET_ALL)
        self.scroll_terminal()

    def stop_spamming(self):
        self.running = False
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        print(Fore.RED + "Mouse Spamming: OFF" + Style.RESET_ALL)
        self.scroll_terminal()

    def spam_mouse(self):
        try:
            controller = mouse.Controller()
            while not self.stop_event.is_set():
                x, y, button = self.click_event
                controller.position = (x, y)
                controller.click(button)
                time.sleep(0.01)  # Adjust the sleep time as needed
        except Exception as e:
            print(Fore.RED + f"Error in spamming thread: {e}" + Style.RESET_ALL)

    def signal_handler(self, sig, frame):
        self.stop_spamming()
        print(Fore.RED + "Exiting..." + Style.RESET_ALL)
        self.listener_keyboard.stop()
        self.listener_mouse.stop()
        sys.exit(0)

    def scroll_terminal(self):
        sys.stdout.write("\n" * 0)
        sys.stdout.flush()

if __name__ == "__main__":
    spammer = MouseSpammer()
    spammer.start()
