import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
import tempfile
from gtts import gTTS

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Personality configurations
PERSONALITIES = {
    "General Assistant": {
        "name": "General Assistant",
        "icon": "🤖",
        "system_prompt": "You are a helpful and friendly AI assistant. You provide clear, accurate, and concise responses to user questions across a wide range of topics."
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "icon": "📚",
        "system_prompt": "You are a supportive study companion. You help students understand concepts, explain topics clearly, provide study tips, and encourage learning. Use examples and break down complex ideas into simpler parts."
    },
    "Fitness Coach": {
        "name": "Fitness Coach",
        "icon": "💪",
        "system_prompt": "You are an enthusiastic fitness coach. You provide workout advice, nutrition tips, motivation, and guidance on healthy lifestyle choices. You encourage users to stay active and make positive health decisions."
    },
    "Gaming Helper": {
        "name": "Gaming Helper",
        "icon": "🎮",
        "system_prompt": "You are a knowledgeable gaming companion. You help with game strategies, tips, recommendations, and gaming culture discussions. You're enthusiastic about games and help players improve their skills."
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design with complementary color theory
st.markdown("""
<style>
    /* Color Palette - Analogous Harmony (Blues and Purples) */
    :root {
        --primary: #4F46E5;        /* Indigo */
        --secondary: #7C3AED;      /* Purple */
        --accent: #06B6D4;         /* Cyan (complementary) */
        --success: #10B981;        /* Green */
        --warning: #F59E0B;        /* Amber */
        --danger: #EF4444;         /* Red */
        --background: #F8FAFC;     /* Light gray */
        --surface: #FFFFFF;        /* White */
        --text-primary: #1E293B;   /* Dark slate */
        --text-secondary: #64748B; /* Slate */
    }

    /* Main container - Light background with subtle gradient */
    .main {
        background: linear-gradient(135deg, #EEF2FF 0%, #F1F5F9 50%, #E0F2FE 100%);
        padding: 2rem;
    }

    /* Improve main block container */
    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* Sidebar - Primary color gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
        box-shadow: 4px 0 24px rgba(79, 70, 229, 0.15);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Button styling with color-coded purposes */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
    }

    .stButton > button:not([kind="primary"]) {
        background-color: var(--surface);
        color: var(--text-primary);
        border: 2px solid var(--accent);
    }

    .stButton > button:not([kind="primary"]):hover {
        background-color: var(--accent);
        color: white;
        transform: translateY(-2px);
    }

    /* Text area with accent border */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #E2E8F0 !important;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
    }

    /* Info boxes with color coding */
    .stInfo {
        background: linear-gradient(135deg, #DBEAFE 0%, #E0F2FE 100%);
        border-left: 4px solid var(--accent);
        border-radius: 12px;
        padding: 1rem;
        color: var(--text-primary) !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border-left: 4px solid var(--success);
        border-radius: 12px;
        color: var(--text-primary) !important;
    }

    .stWarning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border-left: 4px solid var(--warning);
        border-radius: 12px;
        color: var(--text-primary) !important;
    }

    .stError {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        border-left: 4px solid var(--danger);
        border-radius: 12px;
        color: var(--text-primary) !important;
    }

    /* Title with gradient */
    h1 {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    /* Subtitles */
    h2, h3 {
        color: var(--primary);
        font-weight: 700;
    }

    /* Chat message styling - More specific selectors */
    [data-testid="stChatMessage"] {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin: 0.75rem 0 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
        border: 2px solid #E2E8F0 !important;
    }

    /* User messages - Indigo/Purple */
    [data-testid="stChatMessageContent"]:has(+ [data-testid="chatAvatarIcon-user"]),
    .stChatMessage:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%) !important;
        border-left: 5px solid #4F46E5 !important;
    }

    /* Assistant messages - Cyan */
    [data-testid="stChatMessageContent"]:has(+ [data-testid="chatAvatarIcon-assistant"]),
    .stChatMessage:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, #ECFEFF 0%, #CFFAFE 100%) !important;
        border-left: 5px solid #06B6D4 !important;
    }

    /* Ensure chat message content is visible */
    [data-testid="stChatMessageContent"] {
        color: var(--text-primary) !important;
    }

    /* Caption text */
    .stCaption {
        color: var(--text-secondary) !important;
        font-weight: 500;
    }

    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent) 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Spinner color */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }

    /* Mobile-friendly responsive styles */
    @media (max-width: 768px) {
        /* Reduce padding on mobile */
        .stApp {
            padding: 0.5rem !important;
        }

        /* Stack columns on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
        }

        /* Make buttons full width on mobile */
        .stButton > button {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }

        /* Adjust text area height on mobile */
        textarea {
            min-height: 80px !important;
        }

        /* Reduce font sizes slightly on mobile */
        h1 {
            font-size: 1.75rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

        h3 {
            font-size: 1.25rem !important;
        }

        /* Make status cards stack on mobile */
        [data-testid="stHorizontalBlock"] > div {
            flex-direction: column !important;
        }
    }

    /* Tablet styles */
    @media (max-width: 1024px) and (min-width: 769px) {
        .stApp {
            padding: 1rem !important;
        }
    }

    /* Improve audio player responsiveness */
    audio {
        max-width: 100% !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Language support configuration
LANGUAGES = {
    "English": {"code": "en-US", "flag": "🇺🇸", "tts_code": "en", "name": "English"},
    "Spanish": {"code": "es-ES", "flag": "🇪🇸", "tts_code": "es", "name": "Spanish"},
    "French": {"code": "fr-FR", "flag": "🇫🇷", "tts_code": "fr", "name": "French"},
    "German": {"code": "de-DE", "flag": "🇩🇪", "tts_code": "de", "name": "German"},
    "Chinese (Mandarin)": {"code": "zh-CN", "flag": "🇨🇳", "tts_code": "zh-CN", "name": "Chinese (Mandarin)"},
    "Japanese": {"code": "ja-JP", "flag": "🇯🇵", "tts_code": "ja", "name": "Japanese"},
    "Korean": {"code": "ko-KR", "flag": "🇰🇷", "tts_code": "ko", "name": "Korean"},
    "Italian": {"code": "it-IT", "flag": "🇮🇹", "tts_code": "it", "name": "Italian"},
    "Portuguese": {"code": "pt-PT", "flag": "🇵🇹", "tts_code": "pt", "name": "Portuguese"},
    "Russian": {"code": "ru-RU", "flag": "🇷🇺", "tts_code": "ru", "name": "Russian"},
    "Arabic": {"code": "ar-SA", "flag": "🇸🇦", "tts_code": "ar", "name": "Arabic"},
    "Hindi": {"code": "hi-IN", "flag": "🇮🇳", "tts_code": "hi", "name": "Hindi"}
}

# Voice commands configuration
VOICE_COMMANDS = {
    # Chat control commands
    "clear chat": "clear_chat",
    "clear conversation": "clear_chat",
    "delete chat": "clear_chat",
    "erase chat": "clear_chat",

    # Personality change commands
    "change personality to general": "General Assistant",
    "change personality to study": "Study Buddy",
    "change personality to fitness": "Fitness Coach",
    "change personality to gaming": "Gaming Helper",
    "switch to general": "General Assistant",
    "switch to study": "Study Buddy",
    "switch to fitness": "Fitness Coach",
    "switch to gaming": "Gaming Helper",
    "become general assistant": "General Assistant",
    "become study buddy": "Study Buddy",
    "become fitness coach": "Fitness Coach",
    "become gaming helper": "Gaming Helper",

    # TTS speed commands
    "speak slower": "slow_down",
    "slow down": "slow_down",
    "talk slower": "slow_down",
    "speak faster": "speed_up",
    "speed up": "speed_up",
    "talk faster": "speed_up",
    "normal speed": "normal_speed",

    # Help command
    "help": "show_help",
    "show commands": "show_help",
    "what can you do": "show_help",
    "list commands": "show_help"
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

if "voice_activity" not in st.session_state:
    st.session_state.voice_activity = False

if "command_executed" not in st.session_state:
    st.session_state.command_executed = None

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

if "processing" not in st.session_state:
    st.session_state.processing = False

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None

if "tts_speed_slow" not in st.session_state:
    st.session_state.tts_speed_slow = False  # Normal speed by default


# Cache the model creation for faster performance
@st.cache_resource
def get_ai_model(personality, language):
    """Create and cache the AI model for the given personality and language"""
    # Get the base system prompt
    base_prompt = PERSONALITIES[personality]["system_prompt"]

    # Add language instruction if not English
    if language != "English":
        language_name = LANGUAGES[language]["name"]
        language_instruction = f"\n\nIMPORTANT: Please respond in {language_name}. The user will communicate in {language_name}, and you should respond entirely in {language_name}."
        system_prompt = base_prompt + language_instruction
    else:
        system_prompt = base_prompt

    return genai.GenerativeModel(
        'gemini-2.5-flash',
        system_instruction=system_prompt
    )

def generate_tts_audio(text, language="en", slow=False):
    """Generate TTS audio from text using gTTS"""
    try:
        # Create TTS object with speed control
        tts = gTTS(text=text, lang=language, slow=slow)

        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.read()
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.title("AI Chatbot Settings")

    # Personality selector
    selected_personality = st.selectbox(
        "Choose AI Personality",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality)
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history on personality change
        st.rerun()

    # Display personality info
    current_personality = PERSONALITIES[st.session_state.personality]
    st.markdown("---")
    st.markdown(f"### {current_personality['icon']} {current_personality['name']}")
    st.markdown(f"*{current_personality['system_prompt']}*")

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chatbot uses Google's Gemini AI to provide intelligent responses based on the selected personality.")

    st.markdown("---")
    st.markdown("### 🌍 Language Settings")

    # Language selector with flags
    language_options = [f"{LANGUAGES[lang]['flag']} {lang}" for lang in LANGUAGES.keys()]
    selected_lang_display = st.selectbox(
        "Voice Input Language",
        options=language_options,
        index=list(LANGUAGES.keys()).index(st.session_state.selected_language),
        help="Choose the language you'll speak in"
    )

    # Extract language name from selection
    selected_lang = selected_lang_display.split(" ", 1)[1]
    if selected_lang != st.session_state.selected_language:
        st.session_state.selected_language = selected_lang
        # Clear the cached model so it regenerates with new language instruction
        get_ai_model.clear()
        st.success(f"Language changed to {LANGUAGES[selected_lang]['flag']} {selected_lang}")
        st.rerun()

    st.markdown("---")

    # Voice Settings in an expandable section
    with st.expander("🎙️ Voice Settings & Tips", expanded=False):
        st.markdown("""
        **📝 How to Use Voice Input:**
        1. Click the microphone button 🎤
        2. Wait for the red indicator
        3. Speak clearly and naturally
        4. Click again to stop recording

        **🎯 Best Practices:**
        - Speak at a normal conversational pace
        - Position yourself 6-12 inches from microphone
        - Minimize background noise
        - Pause 1 second after finishing

        **🎮 Voice Commands:**
        - "Clear chat" - Erase conversation
        - "Change personality to [name]" - Switch AI mode
        - "Switch to gaming" - Quick personality change

        **⚠️ Troubleshooting:**
        - If recognition fails, try speaking slower
        - Check your language selection matches what you're speaking
        - Ensure microphone permissions are enabled
        - Reduce background noise for better accuracy
        """)

    st.markdown("---")
    # Clear chat button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.tts_audio = {}
        st.rerun()

# Main chat interface
st.title(f"💬 AI Voice Assistant")

# Helpful info box for first-time users
if len(st.session_state.messages) == 0:
    st.info("""
    👋 **Welcome to AI Voice Assistant!**

    - 💬 **Type** your message below or 🎤 **speak** using the microphone button
    - 🔊 **Listen** to AI responses with text-to-speech audio players
    - 🎮 **Try voice commands** like "clear chat" or "switch to gaming"
    - ⚙️ **Customize** personality and language in the sidebar
    """)

# Enhanced status bar with language and personality
status_col1, status_col2 = st.columns(2)
with status_col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
                border-left: 4px solid #4F46E5;
                border-radius: 8px;
                padding: 0.75rem;
                margin-bottom: 1rem;">
        <span style="color: #4F46E5; font-weight: bold;">🤖 Personality:</span>
        <span style="color: #1E293B;"> {st.session_state.personality}</span>
    </div>
    """, unsafe_allow_html=True)

with status_col2:
    current_lang_status = st.session_state.selected_language
    lang_flag_status = LANGUAGES[current_lang_status]['flag']
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ECFEFF 0%, #CFFAFE 100%);
                border-left: 4px solid #06B6D4;
                border-radius: 8px;
                padding: 0.75rem;
                margin-bottom: 1rem;">
        <span style="color: #06B6D4; font-weight: bold;">🌍 Language:</span>
        <span style="color: #1E293B;"> {lang_flag_status} {current_lang_status}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Chat messages section at the top
st.markdown("### 💬 Conversation History")

# Create a container for chat messages
chat_container = st.container()

with chat_container:
    if len(st.session_state.messages) == 0:
        st.info("👋 No messages yet. Start a conversation by typing or using voice input below!")
    else:
        # Display chat messages with custom styling
        for idx, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                # User message with indigo background
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
                            border-left: 5px solid #4F46E5;
                            border-radius: 16px;
                            padding: 1.25rem;
                            margin: 0.75rem 0;
                            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);">
                    <strong style="color: #4F46E5;">👤 You</strong><br>
                    <div style="margin-top: 0.5rem; color: #1E293B;">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Assistant message with cyan background
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ECFEFF 0%, #CFFAFE 100%);
                            border-left: 5px solid #06B6D4;
                            border-radius: 16px;
                            padding: 1.25rem;
                            margin: 0.75rem 0;
                            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);">
                    <strong style="color: #06B6D4;">🤖 AI Assistant</strong><br>
                    <div style="margin-top: 0.5rem; color: #1E293B;">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

                # Display audio player OUTSIDE chat message container
                message_key = f"msg_{idx}"

                # Add visual separator between message and audio
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

                if message_key in st.session_state.tts_audio:
                    # Audio already generated - display it
                    audio_col1, audio_col2 = st.columns([1, 10])
                    with audio_col1:
                        st.markdown("🔊")
                    with audio_col2:
                        st.audio(st.session_state.tts_audio[message_key], format="audio/mp3")
                elif not st.session_state.processing:
                    # Generate TTS audio if not already generated
                    message_length = len(message["content"])

                    # Warn for very long messages
                    if message_length > 500:
                        st.info(f"📝 Long message ({message_length} chars) - audio generation may take a moment...")

                    with st.spinner("🎵 Generating audio..."):
                        try:
                            # Get proper TTS language code from LANGUAGES configuration
                            tts_lang = LANGUAGES[st.session_state.selected_language]["tts_code"]

                            # Truncate extremely long messages for TTS (optional)
                            tts_text = message["content"]
                            if message_length > 1000:
                                tts_text = message["content"][:1000] + "..."
                                st.warning("⚠️ Message truncated to 1000 characters for audio")

                            audio_bytes = generate_tts_audio(tts_text, language=tts_lang, slow=st.session_state.tts_speed_slow)

                            if audio_bytes:
                                st.session_state.tts_audio[message_key] = audio_bytes
                                st.rerun()
                            else:
                                st.error("❌ Audio generation failed. Please refresh or try again.")
                        except Exception as e:
                            st.error(f"❌ TTS Error: {str(e)}")

st.markdown("---")

# Input section at the bottom - always visible
st.markdown("### 💬 Send a Message")

# Show available voice commands in an expandable section
with st.expander("✨ Available Voice Commands", expanded=False):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
                border-radius: 12px;
                padding: 1rem;">
        <h4 style="color: #7C3AED; margin-top: 0;">🎤 Voice Shortcuts</h4>

        <div style="margin-top: 1rem;">
            <strong style="color: #5B21B6;">💬 Chat Control:</strong>
            <ul style="color: #1E293B; margin-top: 0.5rem;">
                <li>"Clear chat" - Erase entire conversation</li>
                <li>"Help" - Show all available commands</li>
            </ul>
        </div>

        <div style="margin-top: 1rem;">
            <strong style="color: #5B21B6;">🎭 Personality Switching:</strong>
            <ul style="color: #1E293B; margin-top: 0.5rem;">
                <li>"Switch to general" - General Assistant</li>
                <li>"Switch to study" - Study Buddy</li>
                <li>"Switch to fitness" - Fitness Coach</li>
                <li>"Switch to gaming" - Gaming Helper</li>
            </ul>
        </div>

        <div style="margin-top: 1rem;">
            <strong style="color: #5B21B6;">🔊 Speech Control:</strong>
            <ul style="color: #1E293B; margin-top: 0.5rem;">
                <li>"Speak slower" - Slow down text-to-speech</li>
                <li>"Speak faster" - Return to normal speed</li>
                <li>"Normal speed" - Reset speech speed</li>
            </ul>
        </div>

        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(124, 58, 237, 0.1); border-radius: 8px;">
            <strong style="color: #7C3AED;">💡 Pro Tip:</strong>
            <span style="color: #1E293B;"> Commands work in any language! Just say them naturally. Say "Help" to see all commands.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Voice input in a compact row
voice_col1, voice_col2, voice_col3 = st.columns([1, 1, 1])

with voice_col2:
    st.markdown("**🎤 Voice Input**")
    audio_bytes = audio_recorder(
        text="",
        recording_color="#EF4444",  # Red when recording
        neutral_color="#3498db",     # Blue when ready
        icon_name="microphone",
        icon_size="2x",
        sample_rate=16000,
        key="audio_recorder"
    )

# Status indicator - compact with language info
current_lang = st.session_state.selected_language
lang_flag = LANGUAGES[current_lang]['flag']

if audio_bytes:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
                border-radius: 8px; margin-top: 0.5rem; animation: pulse 1.5s infinite;">
        <span style="color: #EF4444; font-weight: bold;">🔴 Processing {lang_flag} {current_lang}...</span>
    </div>
    <style>
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
    </style>
    """, unsafe_allow_html=True)
elif st.session_state.voice_text == "":
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #DBEAFE 0%, #E0F2FE 100%);
                border-radius: 8px; margin-top: 0.5rem;">
        <span style="color: #3498db; font-weight: bold;">🎙️ Ready for {lang_flag} {current_lang}</span>
    </div>
    """, unsafe_allow_html=True)

# Show command execution feedback
if st.session_state.command_executed:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.75rem; background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
                border-radius: 12px; margin-top: 0.5rem; border: 2px solid #A855F7;">
        <span style="color: #7C3AED; font-weight: bold;">✨ {st.session_state.command_executed}</span>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.command_executed = None

# VOICE PROCESSING - Completely rewritten
# Process new audio recordings
if audio_bytes:
    # Check if this is new audio by comparing to last processed
    if "last_audio_hash" not in st.session_state:
        st.session_state.last_audio_hash = None

    # Create hash of current audio to detect new recordings
    import hashlib
    current_hash = hashlib.md5(audio_bytes).hexdigest()

    # Only process if this is a new recording
    if current_hash != st.session_state.last_audio_hash:
        st.session_state.last_audio_hash = current_hash

        if len(audio_bytes) < 100:
            st.warning("🔇 Recording too short. Please speak for at least 1 second.")
        else:
            with st.spinner("🎧 Converting speech to text..."):
                try:
                    recognizer = sr.Recognizer()
                    wav_io = io.BytesIO(audio_bytes)

                    with sr.AudioFile(wav_io) as source:
                        audio_data = recognizer.record(source)

                    language_code = LANGUAGES[st.session_state.selected_language]["code"]
                    text = recognizer.recognize_google(audio_data, language=language_code)

                    # Check for voice commands
                    text_lower = text.lower().strip()
                    command_executed = False

                    for command, action in VOICE_COMMANDS.items():
                        if command in text_lower:
                            if action == "clear_chat":
                                st.session_state.messages = []
                                st.session_state.tts_audio = {}
                                st.session_state.command_executed = "Voice Command: Chat Cleared! 🗑️"
                                command_executed = True
                            elif action == "slow_down":
                                st.session_state.tts_speed_slow = True
                                st.session_state.command_executed = "Voice Command: Speech slowed down 🐢"
                                command_executed = True
                            elif action == "speed_up" or action == "normal_speed":
                                st.session_state.tts_speed_slow = False
                                st.session_state.command_executed = "Voice Command: Speech speed normal 🚀"
                                command_executed = True
                            elif action == "show_help":
                                help_message = """**Available Voice Commands:**

**Chat Control:**
- "Clear chat" - Erase conversation
- "Help" - Show this help message

**Personality:**
- "Switch to gaming" - Change to Gaming Helper
- "Switch to study" - Change to Study Buddy
- "Switch to fitness" - Change to Fitness Coach
- "Switch to general" - Change to General Assistant

**Speech Control:**
- "Speak slower" - Slow down text-to-speech
- "Speak faster" - Return to normal speed

Try saying any of these commands naturally!"""
                                st.session_state.messages.append({"role": "assistant", "content": help_message})
                                st.session_state.command_executed = "Voice Command: Help displayed! 💡"
                                command_executed = True
                            elif action in PERSONALITIES:
                                old_personality = st.session_state.personality
                                st.session_state.personality = action
                                st.session_state.command_executed = f"Voice Command: Switched from {old_personality} to {action}! 🎭"
                                command_executed = True
                            break

                    # If no command, set voice text and force update
                    if not command_executed:
                        st.session_state.voice_text = text
                        st.success(f"✅ Voice recognized: \"{text}\"")
                    else:
                        st.session_state.voice_text = ""
                        st.rerun()

                except sr.UnknownValueError:
                    st.error("🤔 Could not understand the audio. Please speak clearly and try again.")
                except sr.RequestError as e:
                    st.error(f"🌐 Could not connect to speech recognition service: {str(e)}")
                except Exception as e:
                    st.error(f"⚠️ Error processing audio: {str(e)}")

# Text input - use voice_text directly
user_input = st.text_area(
    "Message",
    value=st.session_state.voice_text,
    height=100,
    placeholder="✍️ Type your message or use voice input above...",
    key="text_input_area",
    label_visibility="collapsed",
    help="Type your message here or use the microphone button above for voice input"
)

# Send button with better mobile layout
send_col1, send_col2, send_col3 = st.columns([3, 3, 1])
with send_col1:
    if st.button("📤 Send Message", type="primary", use_container_width=True, key="send_btn"):
        if user_input and user_input.strip():
            prompt = user_input.strip()

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Clear inputs and reset audio tracking
            st.session_state.voice_text = ""
            st.session_state.last_audio_hash = None

            # Rerun to show user message immediately
            st.rerun()

with send_col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.voice_text = ""
        st.session_state.last_audio_hash = None
        st.rerun()

# Check if last message needs AI response
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user" and not st.session_state.processing:
    # Set processing flag to prevent duplicate processing
    st.session_state.processing = True

    with st.spinner("🤖 Thinking..."):
        try:
            # Get the last user message
            prompt = st.session_state.messages[-1]["content"]

            # Get cached model for current personality and language
            model = get_ai_model(st.session_state.personality, st.session_state.selected_language)

            # Generate response
            response = model.generate_content(prompt)
            full_response = response.text

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # Reset processing flag
            st.session_state.processing = False

            # Rerun to display the response
            st.rerun()

        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})

            # Reset processing flag
            st.session_state.processing = False

            st.rerun()

# Auto-scroll to bottom using JavaScript
st.markdown("""
<script>
    var element = window.parent.document.querySelector('.main');
    element.scrollTop = element.scrollHeight;
</script>
""", unsafe_allow_html=True)
