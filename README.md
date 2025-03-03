# browsingforall

## Overview

browsingforall is designed to enhance web accessibility through voice commands. It allows physcially challenged users to interact with their web browser using voice commands, making it easier for individuals with disabilities to navigate the web. Built for the Raptors' DEI Hackathon.

## Features

- **Voice Recognition**: Detects wake words and records voice commands.
- **Screenshot Handling**: Captures screenshots of the current browser view.
- **Command Analysis**: Analyzes voice commands using OpenAI's API and extracts UI elements from screenshots using OCR.
- **Action Execution**: Executes actions such as clicking, typing, scrolling, and changing tabs based on the analyzed commands.
- **User Notifications**: Notifies users about various events (e.g., wake word detected, ready to accept command).

## Use Cases for Physically Challenged Folk

- **Hands-Free Browsing**: Allows users with limited mobility to navigate the web using voice commands.
- **Visual Impairment Assistance**: Helps visually impaired users interact with web elements by providing voice feedback and executing commands.
- **Simplified Web Interaction**: Reduces the need for complex keyboard and mouse interactions, making web browsing more accessible.

## How to Use

1. **Start the Application**: Run the main script to start the application.
2. **Wait for Wake Word**: The application listens for a wake word (e.g., "browser").
3. **Give Voice Commands**: After the wake word is detected, give voice commands such as "scroll down", "type hello", or "click on the search bar".
4. **Receive Feedback**: The application will notify you about the actions it performs.

## Setup

### Prerequisites

- Python 3.8
- Tesseract OCR
- OpenAI API Key

### Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/web-accessibility-app.git
    cd web-accessibility-app
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Install Tesseract OCR**:
    - Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
    - Install it to your C: drive (default option)

4. **Set Up Environment Variables**:
    - Create a [.env](http://_vscodecontentref_/2) file in the root directory and add your AIOpen API key:
      ```env
      OPENAI_API_KEY=your_openai_api_key
      ```

### Running the Application

1. **Start the Application**:
    ```sh
    python main.py
    ```

2. **Interact with the Application**:
    - The application will listen for the wake word and execute commands based on your voice input.

## Example Commands

- **Scroll**:
  - "Scroll up"
  - "Scroll down"

- **Change Tab**:
  - "Change to next tab"
  - "Change to previous tab"

- **Type**:
  - "Type hello world"

- **Click**:
  - "Click on the search bar"

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](http://_vscodecontentref_/3) file for details.

## Acknowledgements

- [OpenAI](https://openai.com/) for their powerful API.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for their OCR capabilities.
- [Plyer](https://github.com/kivy/plyer) for desktop notifications.

---

Thank you for using browsingforall! I hope it makes web browsing more accessible and enjoyable for everyone.