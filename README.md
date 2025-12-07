# 💬 AI Voice Assistant

An advanced AI chatbot with comprehensive voice capabilities, built with Streamlit and Google Gemini AI. Features multi-language support, text-to-speech output, intelligent voice commands, and a beautiful modern UI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎤 Voice Input (Speech-to-Text)
- **Google Speech Recognition**: High-accuracy voice transcription
- **12 Languages Supported**: English, Spanish, French, German, Chinese, Japanese, Korean, Italian, Portuguese, Russian, Arabic, Hindi
- **Real-time Feedback**: Visual status indicators and processing feedback
- **Smart Recognition**: Automatic ambient noise adjustment and confidence scoring
- **Edit Before Send**: Review and correct transcriptions before submission
- **No External Dependencies**: Works without ffmpeg installation

### 🔊 Voice Output (Text-to-Speech)
- **Auto-Generated Audio**: AI responses automatically converted to speech
- **Multi-Language TTS**: Supports all 12 interface languages
- **Speed Control**: Adjustable speech speed (normal/slow)
- **Persistent Audio**: Audio players for every AI response
- **Smart Truncation**: Long messages handled gracefully

### 🤖 AI Personalities
Choose from 4 distinct AI personalities powered by Google Gemini:
- **General Assistant** 🤖 - Helpful and friendly for everyday tasks
- **Study Buddy** 📚 - Educational support and learning assistance
- **Fitness Coach** 💪 - Health and fitness guidance
- **Gaming Helper** 🎮 - Game strategies and gaming culture

### 🎮 Voice Commands
Control the chatbot hands-free with natural voice commands:

**Chat Control:**
- "Clear chat" - Erase conversation history
- "Help" - Show all available commands

**Personality Switching:**
- "Switch to general/study/fitness/gaming" - Change AI personality
- "Change personality to [name]" - Alternative syntax
- "Become [personality]" - Quick switch

**Speech Control:**
- "Speak slower" - Slow down text-to-speech
- "Speak faster" - Return to normal speed
- "Normal speed" - Reset speech speed

*Commands work in any selected language!*

### 🌍 Multi-Language Support
Comprehensive language support for both input and output:
- 🇺🇸 English
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇨🇳 Chinese (Mandarin)
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇷🇺 Russian
- 🇸🇦 Arabic
- 🇮🇳 Hindi

### 🎨 Modern UI
- **Beautiful Design**: Gradient color scheme with complementary colors
- **Responsive Layout**: Mobile-friendly with adaptive layouts
- **Custom Chat Bubbles**: Distinct styling for user and AI messages
- **Real-time Status**: Live indicators for language, personality, and activity
- **Smooth Animations**: Polished transitions and loading states
- **Accessibility**: Clear visual feedback and helpful tooltips

### 🚀 Performance
- **Model Caching**: Faster AI responses with cached models
- **Optimized Audio**: Efficient TTS generation and caching
- **Smart Processing**: Asynchronous operations and state management
- **Minimal Latency**: Streamlined message flow

## 🌐 Live Demo

Try the live version of the Voice AI Assistant deployed on Render:

**🎤 [Live Demo on Render](https://voice-ai-assistant-hayhay192.onrender.com/)**

*Note: The app may take 30-60 seconds to wake up if it hasn't been used recently (free tier limitation).*

## 📋 Requirements

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Microphone (for voice input)
- Internet connection
- Modern web browser (Chrome, Firefox, Edge recommended)

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
   - Create a `.env` file in the project root
   - Add your Google Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 Usage Guide

### Getting Started
1. Open the app in your browser
2. Choose your preferred language from the sidebar
3. Select an AI personality (or stick with General Assistant)
4. Start chatting via text or voice!

### Text Chat
1. Type your message in the text area at the bottom
2. Click "📤 Send Message" or press Ctrl+Enter
3. Wait for the AI response
4. Listen to the auto-generated audio or read the text

### Voice Input
1. Click the microphone button 🎤 in the center
2. Wait for the red recording indicator
3. Speak clearly and naturally
4. Click the microphone again to stop recording
5. Review the transcription in the green success box
6. Edit if needed, then click "📤 Send Message"

### Voice Commands
Simply speak commands naturally:
- Say "Help" to see all available commands
- Say "Clear chat" to erase the conversation
- Say "Switch to gaming" to change personality
- Say "Speak slower" to slow down AI speech

### Language Switching
1. Open the sidebar (click the arrow if hidden)
2. Find "🌍 Language Settings"
3. Select your language from the dropdown
4. Voice input, output, and AI responses will all use that language

### Adjusting Settings
- **Personality**: Choose from sidebar dropdown
- **Language**: Select from 12 supported languages
- **Speech Speed**: Use voice commands or set via session
- **Voice Tips**: Expand "🎙️ Voice Settings & Tips" in sidebar

## 📁 Project Structure

```
voice-ai-assistant/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env                   # API key (create this, not in repo)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Technologies Used

### Core Framework
- **Streamlit** - Web application framework
- **Python 3.8+** - Programming language

### AI & Speech
- **Google Gemini 2.5 Flash** - AI conversation model
- **Google Speech Recognition** - Speech-to-text engine
- **gTTS (Google Text-to-Speech)** - Text-to-speech synthesis
- **SpeechRecognition** - Python speech recognition library

### UI Components
- **audio-recorder-streamlit** - Voice input widget
- **Custom CSS** - Styled UI components

## 🎨 Color Scheme

The UI uses a carefully designed analogous color harmony:
- **Primary**: Indigo (#4F46E5) - Main actions and headings
- **Secondary**: Purple (#7C3AED) - Secondary elements
- **Accent**: Cyan (#06B6D4) - Highlights and info
- **Success**: Green (#10B981) - Positive feedback
- **Warning**: Amber (#F59E0B) - Warnings
- **Danger**: Red (#EF4444) - Errors and recording

## 🐛 Troubleshooting

### Voice Input Not Working
- **Check microphone permissions**: Ensure browser has mic access
- **Use HTTPS or localhost**: Voice input requires secure context
- **Audio level indicator**: Should show movement when speaking
- **Reduce background noise**: Speak in a quiet environment
- **Check language selection**: Must match the language you're speaking
- **Position**: Stay 6-12 inches from microphone

### Text-to-Speech Issues
- **No audio player**: Check if TTS generation succeeded (look for errors)
- **Audio not playing**: Try refreshing the page
- **Wrong language**: Ensure language selection matches desired output
- **Speech too fast/slow**: Use voice commands to adjust speed

### API Errors
- **Invalid API key**: Verify your `.env` file has correct key
- **Quota exceeded**: Check your Gemini API usage limits
- **Network issues**: Ensure stable internet connection
- **Rate limiting**: Wait a moment between requests

### Transcription Accuracy
- **Gibberish words**: Speak slower and more clearly
- **Missing words**: Reduce background noise
- **Wrong language detected**: Select correct language in sidebar
- **Partial transcription**: Speak for at least 1 second
- **Ambient noise**: Use the automatic noise adjustment feature

### Performance Issues
- **Slow responses**: Check internet connection speed
- **UI lag**: Close unnecessary browser tabs
- **Audio generation delay**: Normal for long messages (>500 chars)
- **Memory usage**: Clear old conversations periodically

## 💡 Tips & Best Practices

### Voice Input
- Speak at a normal conversational pace
- Articulate clearly but naturally
- Pause for 1 second after finishing
- Minimize background noise
- Position yourself consistently

### Voice Commands
- Commands work in any language
- Say them naturally as part of a sentence
- Most flexible: "Help", "Clear chat", "Switch to [personality]"
- Case-insensitive matching

### Getting Best AI Responses
- Be specific and clear in your questions
- Use appropriate personality for your task
- Provide context when needed
- Try different phrasings if unsatisfied

## 🚀 Advanced Features

### Custom Voice Commands
Edit `VOICE_COMMANDS` dictionary in `app.py` to add your own:
```python
VOICE_COMMANDS = {
    "your custom command": "action_name",
    # Add more commands...
}
```

### Personality Customization
Modify `PERSONALITIES` in `app.py` to create custom AI personalities:
```python
PERSONALITIES = {
    "Your Personality": {
        "name": "Your Personality",
        "icon": "🌟",
        "system_prompt": "Your custom system prompt here..."
    }
}
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs by opening issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit pull requests with fixes
- 🌍 Add support for more languages
- 🎨 Enhance UI/UX design

### Development
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add AmazingFeature'`)
6. Push (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

### Technologies
- [Streamlit](https://streamlit.io/) - Web framework
- [Google Gemini AI](https://deepmind.google/technologies/gemini/) - AI model
- [Google Speech Recognition](https://cloud.google.com/speech-to-text) - Speech-to-text
- [gTTS](https://github.com/pndurette/gTTS) - Text-to-speech
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Python speech library

### Inspiration
Built to demonstrate the power of combining modern AI with intuitive voice interfaces for accessible, natural human-computer interaction.

## 📧 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/CodeCubCA/voice-ai-assistant-hayhay192/issues)
- **Discussions**: Open a GitHub Discussion
- **Documentation**: This README and inline code comments

## 🚢 Deployment

### Deploy to Render

1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your forked repository
4. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your Google Gemini API key
6. Deploy!

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository and branch
5. Add your `GEMINI_API_KEY` in the Secrets section
6. Deploy!

## 🔮 Future Enhancements

Planned features for future releases:
- 🎵 Background music while chatting
- 📊 Conversation analytics and statistics
- 💾 Save/load conversation sessions
- 🌙 Dark/light theme toggle
- 📎 File upload and analysis
- 🔄 Real-time translation mode
- 🎯 Custom wake word detection
- 📱 Mobile app version

## 📊 Project Stats

- **Languages Supported**: 12
- **AI Personalities**: 4
- **Voice Commands**: 30+
- **Lines of Code**: 900+
- **Dependencies**: 6 core libraries

---

**Built with ❤️ using Streamlit and Google Gemini AI**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
