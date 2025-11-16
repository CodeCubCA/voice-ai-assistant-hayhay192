import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
from pydub import AudioSegment
import tempfile

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
</style>
""", unsafe_allow_html=True)

# Language support configuration
LANGUAGES = {
    "English": {"code": "en-US", "flag": "🇺🇸"},
    "Spanish": {"code": "es-ES", "flag": "🇪🇸"},
    "French": {"code": "fr-FR", "flag": "🇫🇷"},
    "German": {"code": "de-DE", "flag": "🇩🇪"},
    "Chinese (Mandarin)": {"code": "zh-CN", "flag": "🇨🇳"},
    "Japanese": {"code": "ja-JP", "flag": "🇯🇵"},
    "Korean": {"code": "ko-KR", "flag": "🇰🇷"},
    "Italian": {"code": "it-IT", "flag": "🇮🇹"},
    "Portuguese": {"code": "pt-PT", "flag": "🇵🇹"},
    "Russian": {"code": "ru-RU", "flag": "🇷🇺"},
    "Arabic": {"code": "ar-SA", "flag": "🇸🇦"},
    "Hindi": {"code": "hi-IN", "flag": "🇮🇳"}
}

# Voice commands configuration
VOICE_COMMANDS = {
    "clear chat": "clear_chat",
    "clear conversation": "clear_chat",
    "delete chat": "clear_chat",
    "erase chat": "clear_chat",
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
    "become gaming helper": "Gaming Helper"
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

# Cache the model creation for faster performance
@st.cache_resource
def get_ai_model(personality):
    """Create and cache the AI model for the given personality"""
    return genai.GenerativeModel(
        'gemini-2.5-flash',
        system_instruction=PERSONALITIES[personality]["system_prompt"]
    )

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
        st.success(f"Language changed to {LANGUAGES[selected_lang]['flag']} {selected_lang}")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎙️ Voice Tips")
    st.markdown("""
    **Recording:**
    - Click mic to start
    - Red = recording
    - Click again to stop

    **Speaking:**
    - Speak slowly for best results
    - Normal conversational volume
    - Pause 1 second after speaking

    **Voice Commands:**
    - "Clear chat" - Erase conversation
    - "Change personality to [name]" - Switch AI mode
    - "Switch to gaming" - Quick personality change
    """)

    st.markdown("---")
    # Clear chat button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title(f"💬 AI Voice Assistant")

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
                <li>"Clear conversation" - Same as above</li>
                <li>"Delete chat" - Remove all messages</li>
            </ul>
        </div>

        <div style="margin-top: 1rem;">
            <strong style="color: #5B21B6;">🎭 Personality Switching:</strong>
            <ul style="color: #1E293B; margin-top: 0.5rem;">
                <li>"Change personality to general" - Switch to General Assistant</li>
                <li>"Switch to study" - Activate Study Buddy</li>
                <li>"Switch to fitness" - Activate Fitness Coach</li>
                <li>"Switch to gaming" - Activate Gaming Helper</li>
                <li>"Become [personality name]" - Quick switch</li>
            </ul>
        </div>

        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(124, 58, 237, 0.1); border-radius: 8px;">
            <strong style="color: #7C3AED;">💡 Pro Tip:</strong>
            <span style="color: #1E293B;"> Commands work in any language! Just say them naturally in your selected language.</span>
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
        sample_rate=16000
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

# Process audio if recorded
if audio_bytes:
    tmp_file_path = None
    try:
        # Check if audio is too short (likely empty/silent)
        if len(audio_bytes) < 1000:  # Less than 1KB is likely just silence
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                        border-left: 5px solid #F59E0B;
                        border-radius: 12px;
                        padding: 1rem;
                        margin-top: 1rem;">
                <div style="color: #D97706; font-weight: bold; font-size: 1.1rem;">
                    🔇 No speech detected
                </div>
                <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                    Your recording was too short or silent. Please try again and speak clearly.
                </div>
                <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                    💡 Tip: Speak for at least 1-2 seconds
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🎧 Processing and converting speech to text..."):
                # Create a temporary WAV file from the audio bytes
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(audio_bytes)
                    tmp_file_path = tmp_file.name

                # Load and process the audio using pydub
                audio = AudioSegment.from_file(tmp_file_path)

                # Voice Activity Detection - analyze audio levels
                audio_level = audio.dBFS
                st.session_state.voice_activity = audio_level > -40

                # Visual feedback for voice activity detection
                if audio_level > -40:
                    activity_color = "#10B981"  # Green - speech detected
                    activity_text = "🟢 Speech Detected"
                elif audio_level > -50:
                    activity_color = "#F59E0B"  # Amber - weak signal
                    activity_text = "🟡 Weak Signal"
                else:
                    activity_color = "#EF4444"  # Red - no speech
                    activity_text = "🔴 No Speech Detected"

                st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem; margin-bottom: 0.5rem;
                            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.2));
                            border-radius: 8px; border: 2px solid {activity_color};">
                    <span style="color: {activity_color}; font-weight: bold;">{activity_text}</span>
                    <div style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; margin-top: 0.5rem; overflow: hidden;">
                        <div style="width: {min(100, max(0, (audio_level + 60) * 2))}%; height: 100%;
                                    background: linear-gradient(90deg, {activity_color}, {activity_color});
                                    transition: width 0.3s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Check if audio is mostly silence
                if audio.dBFS < -50:  # Very quiet audio
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                                border-left: 5px solid #F59E0B;
                                border-radius: 12px;
                                padding: 1rem;
                                margin-top: 1rem;">
                        <div style="color: #D97706; font-weight: bold; font-size: 1.1rem;">
                            🔇 Recording too quiet
                        </div>
                        <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                            No speech detected in your recording. Please try again and speak louder.
                        </div>
                        <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                            💡 Tip: Use your normal speaking voice, 6-12 inches from the mic
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if tmp_file_path:
                        os.unlink(tmp_file_path)
                else:
                    # Convert to mono first for better processing
                    audio = audio.set_channels(1)

                    # AGGRESSIVE noise reduction for background sounds
                    # High-pass filter - removes low frequency background noise (rumble, hum)
                    audio = audio.high_pass_filter(300)  # Increased from 200 to 300 Hz

                    # Low-pass filter - removes high frequency hiss and static
                    audio = audio.low_pass_filter(3000)  # Human voice is typically 300-3000 Hz

                    # Compress dynamic range to focus on nearby sounds
                    # This makes quiet sounds quieter and loud sounds more prominent
                    from pydub.effects import compress_dynamic_range
                    audio = compress_dynamic_range(audio, threshold=-20.0, ratio=4.0, attack=5.0)

                    # Normalize to bring speech to optimal level
                    audio = audio.normalize()

                    # Apply noise gate - only pass audio above certain threshold
                    # This cuts out background noise when you're not speaking
                    def noise_gate(audio_segment, threshold=-35.0):
                        """Apply noise gate to remove quiet background noise"""
                        # Split into chunks
                        chunks = audio_segment[::50]  # 50ms chunks
                        output = AudioSegment.empty()

                        for chunk in chunks:
                            if chunk.dBFS > threshold:
                                output += chunk
                            else:
                                # Replace quiet parts with silence
                                output += AudioSegment.silent(duration=len(chunk))
                        return output

                    audio = noise_gate(audio, threshold=-35.0)

                    # Boost volume slightly for clear speech
                    audio = audio + 6  # Reduced from 10 to 6 dB

                    # Set optimal sample rate for speech recognition
                    audio = audio.set_frame_rate(16000)

                    # Export processed audio to WAV format
                    processed_wav = io.BytesIO()
                    audio.export(processed_wav, format="wav")
                    processed_wav.seek(0)

                    # Use speech recognition
                    recognizer = sr.Recognizer()

                    # Stricter settings to ignore background noise
                    recognizer.energy_threshold = 400  # Increased from 50 - less sensitive to quiet sounds
                    recognizer.dynamic_energy_threshold = True
                    recognizer.dynamic_energy_adjustment_damping = 0.25  # Slower adaptation to noise
                    recognizer.dynamic_energy_ratio = 2.0  # More aggressive noise filtering
                    recognizer.pause_threshold = 0.6  # Slightly longer pauses
                    recognizer.phrase_threshold = 0.5  # Require more speaking time

                    # Load the audio file
                    with sr.AudioFile(processed_wav) as source:
                        # More aggressive ambient noise adjustment
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Increased from 0.2
                        audio_data = recognizer.record(source)

                    # Use Google Speech Recognition with selected language
                    language_code = LANGUAGES[st.session_state.selected_language]["code"]
                    text = recognizer.recognize_google(
                        audio_data,
                        language=language_code,
                        show_all=False
                    )

                    # Check for voice commands (case-insensitive)
                    text_lower = text.lower().strip()
                    command_executed = False

                    for command, action in VOICE_COMMANDS.items():
                        if command in text_lower:
                            if action == "clear_chat":
                                # Clear chat command
                                st.session_state.messages = []
                                st.session_state.command_executed = "Voice Command: Chat Cleared! 🗑️"
                                st.session_state.voice_text = ""
                                command_executed = True
                                st.rerun()
                            elif action in PERSONALITIES:
                                # Change personality command
                                old_personality = st.session_state.personality
                                st.session_state.personality = action
                                st.session_state.command_executed = f"Voice Command: Switched from {old_personality} to {action}! 🎭"
                                st.session_state.voice_text = ""
                                command_executed = True
                                st.rerun()
                            break

                    if not command_executed:
                        st.session_state.voice_text = text

                        # Show success message with transcription
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
                                    border-left: 5px solid #10B981;
                                    border-radius: 12px;
                                    padding: 1rem;
                                    margin-top: 1rem;">
                            <div style="color: #10B981; font-weight: bold; font-size: 1.1rem;">
                                ✅ Ready! Transcription complete ({lang_flag} {current_lang})
                            </div>
                            <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                                <strong>You said:</strong> {text}
                            </div>
                            <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                                💡 Edit the text below if needed, then click Send
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Clean up temp file
                    if tmp_file_path:
                        os.unlink(tmp_file_path)

    except sr.UnknownValueError:
        # Could not understand the audio - friendly message
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                    border-left: 5px solid #F59E0B;
                    border-radius: 12px;
                    padding: 1rem;
                    margin-top: 1rem;">
            <div style="color: #D97706; font-weight: bold; font-size: 1.1rem;">
                🤔 Could not understand your speech
            </div>
            <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                The audio was unclear. Please try again!
            </div>
            <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                💡 Tips: Speak slowly and clearly, reduce background noise, stay close to mic
            </div>
        </div>
        """, unsafe_allow_html=True)
        if tmp_file_path:
            os.unlink(tmp_file_path)

    except sr.RequestError as e:
        # Network/API error - check if it's a permission issue
        error_str = str(e).lower()
        if "permission" in error_str or "access" in error_str or "denied" in error_str:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
                        border-left: 5px solid #EF4444;
                        border-radius: 12px;
                        padding: 1rem;
                        margin-top: 1rem;">
                <div style="color: #DC2626; font-weight: bold; font-size: 1.1rem;">
                    🎤 Microphone access needed
                </div>
                <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                    Please allow microphone access in your browser settings.
                </div>
                <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                    💡 Look for the microphone icon in your browser's address bar and click "Allow"
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Add retry button
            if st.button("🔄 Retry with microphone access", type="secondary", use_container_width=True):
                st.rerun()
        else:
            # Network error
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
                        border-left: 5px solid #EF4444;
                        border-radius: 12px;
                        padding: 1rem;
                        margin-top: 1rem;">
                <div style="color: #DC2626; font-weight: bold; font-size: 1.1rem;">
                    🌐 Connection issue
                </div>
                <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                    Could not connect to the speech recognition service. Please check your internet connection.
                </div>
                <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                    💡 Try again in a moment
                </div>
            </div>
            """, unsafe_allow_html=True)
        if tmp_file_path:
            os.unlink(tmp_file_path)

    except Exception as e:
        # Generic error - don't crash, just show friendly message
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                    border-left: 5px solid #F59E0B;
                    border-radius: 12px;
                    padding: 1rem;
                    margin-top: 1rem;">
            <div style="color: #D97706; font-weight: bold; font-size: 1.1rem;">
                ⚠️ Something went wrong
            </div>
            <div style="color: #1E293B; margin-top: 0.5rem; font-size: 0.95rem;">
                There was an issue processing your recording. Please try recording again.
            </div>
            <div style="color: #64748B; margin-top: 0.5rem; font-size: 0.85rem;">
                💡 If the problem persists, try refreshing the page
            </div>
        </div>
        """, unsafe_allow_html=True)
        if tmp_file_path:
            os.unlink(tmp_file_path)


# Text input section with voice text pre-populated
# Initialize text input in session state if voice text exists
if st.session_state.voice_text and "user_input_text" not in st.session_state:
    st.session_state.user_input_text = st.session_state.voice_text

user_input = st.text_area(
    "Message",
    value=st.session_state.get("user_input_text", st.session_state.voice_text),
    height=100,
    placeholder="✍️ Type your message or use voice input above...",
    key="text_input_area",
    label_visibility="collapsed"
)

# Send button
send_col1, send_col2 = st.columns([4, 1])
with send_col1:
    if st.button("📤 Send Message", type="primary", use_container_width=True, key="send_btn"):
        if user_input and user_input.strip():
            prompt = user_input.strip()

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Clear inputs immediately
            st.session_state.voice_text = ""
            st.session_state.user_input_text = ""

            # Rerun to show user message immediately
            st.rerun()

with send_col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.voice_text = ""
        st.session_state.user_input_text = ""
        st.rerun()

# Check if last message needs AI response
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("🤖 Thinking..."):
        try:
            # Get the last user message
            prompt = st.session_state.messages[-1]["content"]

            # Get cached model for current personality
            model = get_ai_model(st.session_state.personality)

            # Generate response
            response = model.generate_content(prompt)
            full_response = response.text

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # Rerun to display the response
            st.rerun()

        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.rerun()

# Auto-scroll to bottom using JavaScript
st.markdown("""
<script>
    var element = window.parent.document.querySelector('.main');
    element.scrollTop = element.scrollHeight;
</script>
""", unsafe_allow_html=True)
