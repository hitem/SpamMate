# SpamMate
SpamMate is a Python-based macro application designed to record and repeat repetitive keystrokes and mouse inputs. It offers features such as record, preview, replay, and custom delays, allowing for highly customizable automation of repetitive tasks.

## Features
- **Record keystrokes or mouse clicks**: Capture custom sequences with adjustable timing.
- **Replay saved macros**: Automate sequences with replay functionality.
- **Real-time key identification**: Visualize each keystroke for easy verification.
- **Game-specific Profiles**: Includes example profiles for games like Tarisland (`barbarian_dps`, `barbarian_tank`, `cleric_dps`, `cleric_healer`, `stormblade`).
  
## Files

### `spammerk.py`
This script handles **keyboard input** automation. Use this script to record, save, and replay keystroke sequences.
![spammerk](https://github.com/user-attachments/assets/ed207f07-179a-4796-8422-3f3cfae6416d)

#### Keyboard Controls:
- **[`F5`]**: Opens the load window to select an existing profile.
- **[`F6`]**: Starts/stops recording keystrokes. Press `F6` once to start recording, and press `F6` again to stop. The profile is saved to `default.json` by default.
- **[`F7`]**: Exits the application.
- **[`M4`]**: Starts and stop the replay of your recorded keystrokes. *You can rebind this key in the script.*
- **[`F8`]**: Activates key identification mode, displaying each key pressed on screen.

On line 248-250ish you have 2 options to set your prefered delay between keys and the loop.

### `spammerm.py`
This script handles **mouse click** automation, useful for actions such as repetitive clicking in games. \
![spammerk](https://github.com/user-attachments/assets/0116b029-1ae4-4c6d-98cc-cdac196194d2)

#### Mouse Controls:
- **[`F5`]**: Starts and stop the replay of recorded mouse clicks.
- **[`F6`]**: Starts/stops recording mouse clicks. Similar to `spammerk.py`, press `F6` once to start recording and again to stop. The profile is saved to `default.json`.
- **[`F7`]**: Exits the application.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/SpamMate.git
   ```
2. **Navigate to the directory:**
   ```bash
   cd SpamMate
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the keyboard or mouse macro script:**
   - For keyboard macros:
     ```bash
     python3 spammerk.py
     ```
   - For mouse macros:
     ```bash
     python3 spammerm.py
     ```
2. **Use the controls** to start recording, replaying, or exiting as described above.

## Customization

### Changing the Replay Key
- In both `spammerk.py` and `spammerm.py`, you can rebind the default replay key (`M4` for keyboard and `F5` for mouse) by modifying the script directly. Look for the line where the key is defined and change it to your preferred key.

### Creating New Profiles
- When you record a new macro, it is saved as `default.json` unless specified otherwise. You can rename `default.json` to save it as a custom profile (e.g., `game_profile.json`).
- To load a custom profile, press `F5` and select from the available JSON files in the application directory.

## Example Profiles
Example profiles for games like Tarisland are included:
- `barbarian_dps.json`
- `barbarian_tank.json`
- `cleric_dps.json`
- `cleric_healer.json`
- `stormblade.json`

These profiles can be loaded using `F5` in the spammerm script if located in the root folder.
