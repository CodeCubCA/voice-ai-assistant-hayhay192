# 💬 AI Voice Assistant

An advanced AI chatbot with voice input capabilities, built with Streamlit and Google Gemini AI. Features multi-language support, voice commands, and a beautiful modern UI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎤 Voice Input
- **Speech-to-Text**: Convert your voice to text using Google Speech Recognition
- **12 Languages Supported**: English, Spanish, French, German, Chinese, Japanese, Korean, Italian, Portuguese, Russian, Arabic, Hindi
- **Voice Activity Detection**: Real-time audio level monitoring with visual feedback
- **Noise Reduction**: Advanced audio processing to filter background noise
- **Smart Recognition**: Automatic ambient noise adjustment

### 🤖 AI Personalities
Choose from 4 distinct AI personalities:
- **General Assistant** 🤖 - Helpful and friendly for everyday tasks
- **Study Buddy** 📚 - Educational support and learning assistance
- **Fitness Coach** 💪 - Health and fitness guidance
- **Gaming Helper** 🎮 - Game strategies and gaming culture

### ✨ Voice Commands
Control the chatbot with your voice:
- `"Clear chat"` - Erase conversation history
- `"Change personality to [name]"` - Switch AI personality
- `"Switch to gaming"` - Quick personality switching

### 🎨 Modern UI
- Beautiful gradient design with color theory
- Responsive layout
- Custom-styled chat bubbles
- Real-time status indicators
- Smooth animations and transitions

### 🚀 Performance
- Model caching for faster responses
- Optimized message flow
- Asynchronous UI updates
- Minimal latency

## 📋 Requirements

- Python 3.8 or higher
- Google Gemini API key
- Microphone (for voice input)
- Internet connection

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/CodeCubCA/voice-ai-assistant-hayhay192.git
cd voice-ai-assistant-hayhay192
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**
   - Copy `.env.example` to `.env`
   - Add your Google Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Usage

### Text Input
1. Type your message in the text area
2. Click "📤 Send Message"
3. Wait for the AI response

### Voice Input
1. Click the microphone button 🎤
2. Speak clearly when the button turns red
3. Click again to stop recording
4. Review the transcription
5. Edit if needed and click "Send"

### Voice Commands
Simply say commands naturally:
- "Clear chat" to erase the conversation
- "Switch to gaming" to change personality
- Commands work in any selected language!

### Language Selection
1. Open the sidebar
2. Choose your language from the dropdown
3. The voice input will now recognize that language

## 📁 Project Structure

```
voice-ai-assistant/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env                   # API key (not in repo)
├── .env.example          # API key template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

### Supported Languages
- 🇺🇸 English (en-US)
- 🇪🇸 Spanish (es-ES)
- 🇫🇷 French (fr-FR)
- 🇩🇪 German (de-DE)
- 🇨🇳 Chinese Mandarin (zh-CN)
- 🇯🇵 Japanese (ja-JP)
- 🇰🇷 Korean (ko-KR)
- 🇮🇹 Italian (it-IT)
- 🇵🇹 Portuguese (pt-PT)
- 🇷🇺 Russian (ru-RU)
- 🇸🇦 Arabic (ar-SA)
- 🇮🇳 Hindi (hi-IN)

### Voice Commands
Edit `VOICE_COMMANDS` in `app.py` to add custom commands:
```python
VOICE_COMMANDS = {
    "your command": "action",
    # Add more commands...
}
```

## 🎨 Color Scheme

The UI uses an analogous color harmony:
- **Primary**: Indigo (#4F46E5)
- **Secondary**: Purple (#7C3AED)
- **Accent**: Cyan (#06B6D4)
- **Success**: Green (#10B981)
- **Warning**: Amber (#F59E0B)
- **Danger**: Red (#EF4444)

## 🐛 Troubleshooting

### Voice input not working
- Check microphone permissions in your browser
- Ensure you're using HTTPS or localhost
- Try speaking louder and closer to the microphone
- Check the audio level indicator

### API errors
- Verify your API key in `.env`
- Check your internet connection
- Ensure you haven't exceeded API quotas

### Transcription issues
- Reduce background noise
- Speak slowly and clearly
- Check selected language matches what you're speaking
- Position yourself 6-12 inches from the microphone

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Speech recognition by [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- Audio processing with [Pydub](https://github.com/jiaaro/pydub)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
