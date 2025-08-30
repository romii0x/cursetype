```text
                          ▄▄· ▄• ▄▌▄▄▄  .▄▄ · ▄▄▄ .▄▄▄▄▄ ▄· ▄▌ ▄▄▄·▄▄▄ .
                         ▐█ ▌▪█▪██▌▀▄ █·▐█ ▀. ▀▄.▀·•██  ▐█▪██▌▐█ ▄█▀▄.▀·
                         ██ ▄▄█▌▐█▌▐▀▀▄ ▄▀▀▀█▄▐▀▀▪▄ ▐█.▪▐█▌▐█▪ ██▀·▐▀▀▪▄
                         ▐███▌▐█▄█▌▐█•█▌▐█▄▪▐█▐█▄▄▌ ▐█▌· ▐█▀·.▐█▪·•▐█▄▄▌
                         ·▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀▀  ▀▀▀  ▀▀▀   ▀ • .▀    ▀▀▀ 
```
**CurseType** is a terminal-based typing test built with Python's `curses` library. It provides real-time performance feedback, multiple difficulty levels, and customizable colors.

![cursetype](https://github.com/user-attachments/assets/859a7ff6-b417-4793-be52-8ec4c5fdb001)

## Features

### **Typing Modes**
- **Sentence Mode**: Practice with single sentences for quick typing sessions
- **Paragraph Mode**: Multi-line typing tests for extended practice sessions

### **Real-Time Performance Tracking**
- **WPM (Words Per Minute)**: Live calculation of typing speed
- **Accuracy Percentage**: Real-time accuracy tracking with color-coded feedback
- **Character Statistics**: Detailed breakdown of correct/incorrect characters and corrections made

### **Customizable Interface**
- **Color Customization**: Choose colors for correct letters, incorrect letters, and menu elements
- **Dynamic Color Feedback**: Performance-based color changes (blue -> green -> yellow -> red)

### **Multiple Difficulty Levels**
- **MonkeyType Default**: 200 most common English words (matches MonkeyType's default)
- **English 1000**: 1,000 most common English words
- **Oxford 3000**: English 1000 + Oxford 3000 word list
- **Oxford 5000**: All word lists (Oxford 5000 + English 1000 + Oxford 3000)

## Requirements

- **Python**: 3.7 or higher
- **Terminal**: Unix-like terminal environment (Linux, macOS, or WSL on Windows)
- **Minimum Terminal Size**: 65x15 characters

## Installation & Usage

### Linux & macOS

```bash
# Clone the repository
git clone https://github.com/romii0x/cursetype.git

# Change to the project directory
cd cursetype

# Run the program
python3 main.py
```
### Windows (via WSL)

CurseType requires a Unix-like terminal environment. On Windows, use the Windows Subsystem for Linux (WSL):

1. **Install WSL** by following the [official guide](https://learn.microsoft.com/en-us/windows/wsl/install)
2. **Open your WSL terminal** and follow the Linux & macOS installation steps above

## How to Use

### Getting Started
1. **Launch the application**: Run `python3 main.py`
2. **Navigate the menu**: Use arrow keys (↑↓) or vim-style navigation (j/k)
3. **Select options**: Press Enter to confirm selections
4. **Exit**: Use Home or Delete keys to return to previous menus

### Typing Test Interface
- **Type the highlighted text**: The current character is underlined and bold
- **Real-time feedback**: WPM and accuracy update as you type
- **Error handling**: Incorrect characters are highlighted in red
- **Backspace**: Use backspace to correct mistakes
- **Complete the test**: Type all characters to see your final results

### Settings & Customization
- **Color Settings**: Customize colors for correct/incorrect letters and menus
- **Difficulty Settings**: Choose from three vocabulary difficulty levels
- **Color Picker**: Interactive grid-based color selection interface

### Controls
- **Arrow Keys**: Navigate menus and color picker
- **Enter**: Select/confirm options
- **Home/Delete**: Go back/exit
- **Backspace**: Correct typing mistakes
- **Any other key**: Type characters during tests

## Technical Details

### Architecture
- **Modular Design**: Clean separation of concerns across multiple modules
- **Configuration Management**: INI-based settings with automatic defaults
- **Error Handling**: Robust error handling for file operations and user input
- **Performance Optimization**: Efficient character-by-character processing

### Word Lists
- **monkeytype-200.txt**: 200 most common English words (MonkeyType default)
- **english-1000.txt**: 1,000 most common English words
- **oxford-3000.txt**: Oxford 3000 word list
- **oxford-5000.txt**: Oxford 5000 word list

### Performance Metrics
- **WPM Calculation**: Based on average word length and typing time
- **Accuracy**: Percentage of correctly typed characters
- **Character Tracking**: Separate counters for total and final character counts

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License & Credits

- **License**: [LICENSE.txt](LICENSE.txt)
- **Word Lists**: 
  - [Oxford 3000/5000](https://github.com/tgmgroup/Word-List-from-Oxford-Longman-5000)
  - [English 1000](https://gist.github.com/deekayen/4148741)
  - [MonkeyType 200](https://github.com/monkeytypegame/monkeytype/blob/master/frontend/static/languages/english.json)