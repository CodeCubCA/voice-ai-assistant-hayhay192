#!/usr/bin/env python3
"""
Test script to verify voice processing works correctly.
This simulates what the Streamlit app does with voice input.
"""

import speech_recognition as sr
import tempfile
import os
import sys

def test_audio_processing():
    """Test the audio processing pipeline"""
    print("=" * 60)
    print("VOICE PROCESSING TEST")
    print("=" * 60)

    # Test 1: Check if SpeechRecognition is working
    print("\n[TEST 1] Testing SpeechRecognition library...")
    try:
        recognizer = sr.Recognizer()
        print("✅ SpeechRecognition initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize SpeechRecognition: {e}")
        return False

    # Test 2: Test with microphone (record a short audio)
    print("\n[TEST 2] Testing microphone recording...")
    print("Please say something when prompted...")

    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise... (please be quiet)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🔴 Recording... Speak now!")
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("✅ Audio recorded successfully")

            # Save the audio to a temp file to simulate what audio-recorder-streamlit does
            print("\n[TEST 3] Saving audio to temporary WAV file...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wav_data = audio_data.get_wav_data()
                tmp.write(wav_data)
                tmp_file = tmp.name
                print(f"✅ Audio saved to: {tmp_file}")
                print(f"   File size: {len(wav_data)} bytes")

            # Test 4: Load the WAV file back (simulate Streamlit app behavior)
            print("\n[TEST 4] Loading WAV file with sr.AudioFile()...")
            try:
                with sr.AudioFile(tmp_file) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    loaded_audio = recognizer.record(source)
                    print("✅ WAV file loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load WAV file: {e}")
                os.unlink(tmp_file)
                return False

            # Test 5: Try to recognize the speech
            print("\n[TEST 5] Attempting speech recognition with Google API...")
            try:
                # First try with show_all=True (like the app does)
                result = recognizer.recognize_google(loaded_audio, language="en-US", show_all=True)
                print(f"✅ Recognition succeeded!")
                print(f"   Result type: {type(result)}")
                print(f"   Result: {result}")

                if result and len(result) > 0:
                    text = result[0]['transcript']
                    confidence = result[0].get('confidence', 'N/A')
                    print(f"\n📝 TRANSCRIPTION: '{text}'")
                    print(f"   Confidence: {confidence}")
                else:
                    print("⚠️  Empty result from Google API")

            except sr.UnknownValueError:
                print("❌ Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Could not request results from Google Speech Recognition: {e}")
            except Exception as e:
                print(f"❌ Unexpected error during recognition: {type(e).__name__}: {e}")

            # Cleanup
            print(f"\n[CLEANUP] Removing temporary file...")
            os.unlink(tmp_file)
            print("✅ Cleanup complete")

            print("\n" + "=" * 60)
            print("TEST COMPLETE")
            print("=" * 60)
            return True

    except sr.WaitTimeoutError:
        print("❌ Timeout - no speech detected")
        return False
    except Exception as e:
        print(f"❌ Error during recording: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\nThis test will:")
    print("1. Record audio from your microphone")
    print("2. Save it to a WAV file (simulating audio-recorder-streamlit)")
    print("3. Load the WAV file and process it")
    print("4. Send it to Google Speech Recognition")
    print("\nMake sure your microphone is working and you're in a quiet environment.")
    input("\nPress Enter to start the test...")

    success = test_audio_processing()
    sys.exit(0 if success else 1)
