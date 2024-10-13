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
print(Fore.LIGHTMAGENTA_EX + "  [" + Fore.RED + "F5" + Fore.LIGHTMAGENTA_EX + "] Load    [" + Fore.RED + "F6" +
      Fore.LIGHTMAGENTA_EX + "] Record    [" + Fore.RED + "F7" + Fore.LIGHTMAGENTA_EX + "] Exit   " + Fore.RESET)
print(Fore.LIGHTMAGENTA_EX + "  [" + Fore.RED + "M4" + Fore.LIGHTMAGENTA_EX +
      "] Replay  [" + Fore.RED + "F8" + Fore.LIGHTMAGENTA_EX + "] Identify Keys" + Fore.RESET)
print("")
print(Fore.YELLOW + "→ by hitem                              🖮" + Fore.RESET)
print("------------------------------------------")


class KeySpammer:
    def __init__(self, max_events=1000, save_file='default.json'):
        self.running = False
        self.capturing = False
        self.selecting_json = False
        self.identifying_keys = False
        self.listener_keyboard = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.listener_mouse = mouse.Listener(on_click=self.on_click)
        self.key_events = []
        self.max_events = max_events
        self.save_file = save_file
        self.stop_event = threading.Event()  # Initialize stop_event here
        self.thread = None  # Initialize thread here
        self.check_for_json_files()

    def check_for_json_files(self):
        json_files = [file for file in os.listdir() if file.endswith('.json')]
        if not json_files:
            print(Fore.YELLOW + "No saved key events found." + Style.RESET_ALL)
            print(Fore.CYAN + "Press F5 to select a JSON file." + Style.RESET_ALL)
        elif len(json_files) == 1:
            self.save_file = json_files[0]
            self.load_key_events()  # Load key events here if there's only one file
        else:
            self.select_json_file(json_files)

    def load_key_events(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                self.key_events = json.load(f)
                self.key_events = [(action, self.deserialize_key(key))
                                   for action, key in self.key_events]
            print(
                Fore.GREEN + f"Loaded {len(self.key_events)//2} key events from {self.save_file}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Ready to record new events." + Style.RESET_ALL)

    def save_key_events(self):
        with open(self.save_file, 'w') as f:
            json.dump([(action, self.serialize_key(key))
                      for action, key in self.key_events], f)
        print(
            Fore.GREEN + f"Saved {len(self.key_events)//2} key events to {self.save_file}" + Style.RESET_ALL)

    def serialize_key(self, key):
        if isinstance(key, keyboard.KeyCode):
            return {'type': 'KeyCode', 'char': key.char}
        elif isinstance(key, keyboard.Key):
            return {'type': 'Key', 'name': key.name}
        else:
            raise TypeError(f'Unsupported key type: {type(key)}')

    def deserialize_key(self, key):
        if key['type'] == 'KeyCode':
            return keyboard.KeyCode(char=key['char'])
        elif key['type'] == 'Key':
            return getattr(keyboard.Key, key['name'])
        else:
            raise TypeError(f'Unsupported key type: {key["type"]}')

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        print(Fore.RED + "Key Spamming: OFF" + Style.RESET_ALL)
        self.listener_keyboard.start()
        self.listener_mouse.start()
        self.listener_keyboard.join()
        self.listener_mouse.join()

    def on_click(self, x, y, button, pressed):
            if button == mouse.Button.x1 and pressed:
                self.toggle_spamming()
            if self.identifying_keys and pressed:
                print(Fore.BLUE + f"Mouse Button Pressed: {button}" + Style.RESET_ALL)

    def on_press(self, key):
        try:
            # Ignore control keys used for starting/stopping recording
            if key in [keyboard.Key.f5, keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8]:
                if key == keyboard.Key.f5 and not self.selecting_json:
                    self.select_json_file()
                elif key == keyboard.Key.f6:
                    self.toggle_capture()
                elif key == keyboard.Key.f7:
                    self.signal_handler(None, None)
                elif key == keyboard.Key.f8:
                    self.toggle_identify_keys()
                return  # Ignore these keys for recording purposes
            if self.capturing:
                if len(self.key_events) < self.max_events:
                    self.key_events.append(('press', key))
                else:
                    print(
                        Fore.YELLOW + "Maximum number of events reached. Stopping capture." + Style.RESET_ALL)
                    self.toggle_capture()
            if self.identifying_keys:
                print(Fore.BLUE + f"Key Pressed: {key}" + Style.RESET_ALL)
        except AttributeError:
            pass
        
    def on_release(self, key):
        # Ignore control keys used for starting/stopping recording
        if key in [keyboard.Key.f5, keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8]:
            return  # Ignore these keys for recording purposes
        if self.capturing and len(self.key_events) < self.max_events:
            self.key_events.append(('release', key))
    
        def on_click(self, x, y, button, pressed):
            if button == mouse.Button.x1 and pressed:
                self.toggle_spamming()
            if self.identifying_keys and pressed:
                print(Fore.BLUE +
                      f"Mouse Button Pressed: {button}" + Style.RESET_ALL)

    def select_json_file(self, json_files=None):
        self.stop_spamming()  # Ensure spamming is stopped before selecting new JSON file
        self.selecting_json = True
        if json_files is None:
            json_files = [file for file in os.listdir()
                          if file.endswith('.json')]
        if len(json_files) > 1:
            print(Fore.CYAN + "Please select a JSON file to load:" + Style.RESET_ALL)
            for idx, file in enumerate(json_files):
                print(Fore.CYAN + f"{idx + 1}. " +
                      Fore.WHITE + f"{file}" + Style.RESET_ALL)
            while True:
                try:
                    choice = int(input(
                        Fore.CYAN + "Enter the number of the file you want to load: " + Style.RESET_ALL))
                    if 1 <= choice <= len(json_files):
                        self.save_file = json_files[choice - 1]
                        self.load_key_events()  # Load key events after selecting the file
                        break
                    else:
                        print(
                            Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
                except ValueError:
                    print(
                        Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
        elif len(json_files) == 1:
            self.save_file = json_files[0]
            self.load_key_events()

        self.selecting_json = False

    def toggle_capture(self):
        if not self.running:
            self.capturing = not self.capturing
            if self.capturing:
                # Delete the JSON file when starting a new capture
                if os.path.exists(self.save_file):
                    os.remove(self.save_file)
                self.key_events = []  # Clear previous recordings
                print(Fore.CYAN + "Capture Mode: ON" + Style.RESET_ALL)
            else:
                print(Fore.CYAN + "Capture Mode: OFF" + Style.RESET_ALL)
                print(
                    Fore.BLUE + f"Captured {len(self.key_events)//2} key events" + Style.RESET_ALL)
                self.save_key_events()
            self.scroll_terminal()

    def toggle_spamming(self):
        if self.capturing:
            print(Fore.YELLOW +
                  "Cannot start spamming while capturing" + Style.RESET_ALL)
            return
        if self.running:
            self.stop_spamming()
        else:
            self.start_spamming()
        self.scroll_terminal()

    def toggle_identify_keys(self):
        self.identifying_keys = not self.identifying_keys
        if self.identifying_keys:
            print(Fore.CYAN + "Identify Keys Mode: ON" + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "Identify Keys Mode: OFF" + Style.RESET_ALL)

    def start_spamming(self):
        if not self.key_events:
            print(Fore.YELLOW + "No keys captured yet!" + Style.RESET_ALL)
            return
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.spam_keys)
        self.thread.start()
        print(Fore.GREEN + "Key Spamming: ON" + Style.RESET_ALL)
        self.scroll_terminal()

    def stop_spamming(self):
        self.running = False
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        print(Fore.RED + "Key Spamming: OFF" + Style.RESET_ALL)
        self.scroll_terminal()

    def spam_keys(self):
        try:
            controller = keyboard.Controller()
            while not self.stop_event.is_set():
                for event in self.key_events:
                    if self.stop_event.is_set():
                        break
                    action, key = event
                    if action == 'press':
                        controller.press(key)
                    elif action == 'release':
                        controller.release(key)
                    # Adjust the sleep time as needed between key events
                    time.sleep(0.08)
                # Adjust the sleep time between loops as needed
                time.sleep(0.25)
        except Exception as e:
            print(
                Fore.RED + f"Error in spamming thread: {e}" + Style.RESET_ALL)

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
    spammer = KeySpammer()
    spammer.start()
