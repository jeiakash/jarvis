# Create a test script
import speech_recognition as sr

def test_all_microphones():
    r = sr.Recognizer()
    
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")
    
    # Test specific microphones that are likely to work
    test_indices = [11, 0, 6, None]  # PulseAudio, HDA Analog, DMIC, Default
    
    for device_index in test_indices:
        try:
            print(f"\nTesting microphone {device_index}...")
            with sr.Microphone(device_index=device_index) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Say something for 3 seconds...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                
            try:
                text = r.recognize_google(audio)
                print(f"SUCCESS! Microphone {device_index} recognized: {text}")
                return device_index
            except sr.UnknownValueError:
                print(f"Microphone {device_index} works but couldn't understand speech")
            except sr.RequestError as e:
                print(f"Recognition service error: {e}")
                
        except Exception as e:
            print(f"Microphone {device_index} failed: {e}")
    
    return None

if __name__ == "__main__":
    working_mic = test_all_microphones()
    if working_mic is not None:
        print(f"\nUse device_index={working_mic} in your Jarvis script")
    else:
        print("\nNo working microphone found")
