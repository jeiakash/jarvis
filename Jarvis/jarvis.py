import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyjokes
import subprocess
import sys
import urllib.parse
import signal
import time

class VoiceAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.assistant_name = self.load_name()
        self.waiting_for_wikipedia_query = False
        self.waiting_for_google_query = False
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\nShutting down gracefully...")
        self.speak("Goodbye!")
        sys.exit(0)
        
    def setup_voice(self):
        """Configure voice settings"""
        try:
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)  # Female voice
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1)
        except Exception as e:
            print(f"Voice setup error: {e}")

    def speak(self, audio):
        """Convert text to speech with error handling"""
        try:
            print(f"Assistant: {audio}")
            self.engine.say(audio)
            self.engine.runAndWait()
        except KeyboardInterrupt:
            # Handle interruption gracefully
            self.engine.stop()
            raise
        except Exception as e:
            print(f"Speech error: {e}")

    def get_time(self):
        """Get current time"""
        try:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            message = f"The current time is {current_time}"
            self.speak(message)
        except Exception as e:
            self.speak("Sorry, I couldn't get the time")
            print(f"Time error: {e}")

    def get_date(self):
        """Get current date"""
        try:
            now = datetime.datetime.now()
            date_str = now.strftime("%B %d, %Y")
            message = f"Today is {date_str}"
            self.speak(message)
        except Exception as e:
            self.speak("Sorry, I couldn't get the date")
            print(f"Date error: {e}")

    def greet_user(self):
        """Greet user based on time of day"""
        self.speak("Welcome back, sir!")
        
        hour = datetime.datetime.now().hour
        if 4 <= hour < 12:
            self.speak("Good morning!")
        elif 12 <= hour < 16:
            self.speak("Good afternoon!")
        elif 16 <= hour < 24:
            self.speak("Good evening!")
        else:
            self.speak("Good night!")
            
        self.speak(f"{self.assistant_name} at your service. How may I assist you?")

    def take_screenshot(self):
        """Automatically take a screenshot when commanded"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"screenshot_{timestamp}.png"
            screenshot_path = os.path.join(os.getcwd(), screenshot_name)
            
            print("Taking screenshot automatically...")
            self.speak("Taking screenshot now")
            
            # Method 1: Try using gnome-screenshot with automatic save
            try:
                print("Attempting automatic screenshot...")
                
                # Create a script that will run gnome-screenshot in the current desktop session
                script_content = f'''#!/bin/bash
export DISPLAY=:0
cd "{os.getcwd()}"
gnome-screenshot -f "{screenshot_name}"
'''
                
                # Write the script to a temporary file
                script_path = "/tmp/take_screenshot.sh"
                with open(script_path, 'w') as f:
                    f.write(script_content)
                
                # Make it executable
                os.chmod(script_path, 0o755)
                
                # Execute the script
                result = subprocess.run(['bash', script_path], timeout=10)
                
                # Check if screenshot was created
                if os.path.exists(screenshot_path):
                    self.speak(f"Screenshot saved as {screenshot_name}")
                    print(f"Screenshot saved: {screenshot_path}")
                    return True
                    
            except Exception as e:
                print(f"Method 1 failed: {e}")
            
            # Method 2: Try using scrot directly
            try:
                print("Trying scrot method...")
                env = os.environ.copy()
                env['DISPLAY'] = ':0'
                
                result = subprocess.run(
                    ['scrot', screenshot_path], 
                    env=env,
                    timeout=10,
                    capture_output=True
                )
                
                if os.path.exists(screenshot_path):
                    self.speak(f"Screenshot captured successfully")
                    print(f"Screenshot saved: {screenshot_path}")
                    return True
                    
            except Exception as e:
                print(f"Scrot method failed: {e}")
            
            # Method 3: Try using import from ImageMagick
            try:
                print("Trying ImageMagick import...")
                env = os.environ.copy()
                env['DISPLAY'] = ':0'
                
                result = subprocess.run(
                    ['import', '-window', 'root', screenshot_path], 
                    env=env,
                    timeout=10,
                    capture_output=True
                )
                
                if os.path.exists(screenshot_path):
                    self.speak(f"Screenshot taken with ImageMagick")
                    print(f"Screenshot saved: {screenshot_path}")
                    return True
                    
            except Exception as e:
                print(f"ImageMagick method failed: {e}")
            
            # Method 4: Try using a different approach with xvfb-run
            try:
                print("Trying xvfb-run method...")
                result = subprocess.run([
                    'xvfb-run', '-a', '-s', '-screen 0 1024x768x24',
                    'gnome-screenshot', '-f', screenshot_path
                ], timeout=15, capture_output=True)
                
                if os.path.exists(screenshot_path):
                    self.speak("Screenshot captured using virtual display")
                    print(f"Screenshot saved: {screenshot_path}")
                    return True
                    
            except Exception as e:
                print(f"xvfb-run method failed: {e}")
            
            # Method 5: Try using Python PIL with different approach
            try:
                print("Trying Python PIL method...")
                import PIL.ImageGrab as ImageGrab
                
                # Try to grab the screen
                screenshot = ImageGrab.grab()
                screenshot.save(screenshot_path)
                
                if os.path.exists(screenshot_path):
                    self.speak("Screenshot taken using Python")
                    print(f"Screenshot saved: {screenshot_path}")
                    return True
                    
            except Exception as e:
                print(f"PIL method failed: {e}")
            
            # If all methods fail, try one more approach
            self.try_alternative_screenshot_method(screenshot_name)
            
        except Exception as e:
            self.speak("Sorry, I couldn't take the screenshot automatically")
            print(f"Screenshot error: {e}")
            return False

    def try_alternative_screenshot_method(self, screenshot_name):
        """Try alternative screenshot methods"""
        try:
            print("Trying alternative methods...")
            
            # Method: Use dbus to call gnome-screenshot
            try:
                print("Trying dbus method...")
                subprocess.run([
                    'dbus-send', '--session', '--dest=org.gnome.Shell.Screenshot',
                    '--type=method_call', '/org/gnome/Shell/Screenshot',
                    'org.gnome.Shell.Screenshot.Screenshot',
                    'boolean:true', 'boolean:false', f'string:{screenshot_name}'
                ], timeout=10)
                
                if os.path.exists(screenshot_name):
                    self.speak("Screenshot taken using system service")
                    return True
                    
            except Exception as e:
                print(f"dbus method failed: {e}")
            
            # Method: Use grim (for Wayland)
            try:
                print("Trying grim for Wayland...")
                result = subprocess.run(['grim', screenshot_name], timeout=10, capture_output=True)
                
                if os.path.exists(screenshot_name):
                    self.speak("Screenshot taken using Wayland")
                    return True
                    
            except Exception as e:
                print(f"grim method failed: {e}")
            
            # Final fallback: Create a simple script for user to run
            self.create_screenshot_script(screenshot_name)
            
        except Exception as e:
            print(f"Alternative methods failed: {e}")

    def create_screenshot_script(self, screenshot_name):
        """Create a script that user can run to take screenshot"""
        try:
            script_content = f'''#!/bin/bash
echo "Taking screenshot..."
gnome-screenshot -f {screenshot_name}
echo "Screenshot saved as {screenshot_name}"
'''
            
            script_path = "take_screenshot_now.sh"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            os.chmod(script_path, 0o755)
            
            self.speak("I've created a screenshot script. Please run the script take_screenshot_now.sh in a new terminal")
            print(f"Created script: {script_path}")
            print("Run this command in a new terminal: ./take_screenshot_now.sh")
            
        except Exception as e:
            print(f"Script creation failed: {e}")
            self.speak("Please use the Print Screen key to take a screenshot")

    def listen_command(self):
        """Listen for voice commands"""
        r = sr.Recognizer()
        
        # Suppress ALSA warnings by redirecting stderr
        with open(os.devnull, 'w') as devnull:
            old_stderr = os.dup(2)
            os.dup2(devnull.fileno(), 2)
            
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    r.pause_threshold = 1
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    
            except sr.WaitTimeoutError:
                return None
            except Exception as e:
                print(f"Microphone error: {e}")
                return None
            finally:
                # Restore stderr
                os.dup2(old_stderr, 2)
                os.close(old_stderr)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
            
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that")
            return None
        except sr.RequestError:
            self.speak("Speech recognition service is unavailable")
            return None
        except Exception as e:
            print(f"Recognition error: {e}")
            return None

    def play_music(self, song_name=None):
        """Play music from Music directory"""
        try:
            music_dir = os.path.expanduser("~/Music")
            if not os.path.exists(music_dir):
                self.speak("Music directory not found")
                return
                
            songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.flac', '.ogg'))]
            
            if song_name:
                songs = [song for song in songs if song_name.lower() in song.lower()]
                
            if songs:
                song = random.choice(songs)
                song_path = os.path.join(music_dir, song)
                
                if sys.platform.startswith('linux'):
                    subprocess.Popen(['xdg-open', song_path])
                elif sys.platform.startswith('win'):
                    os.startfile(song_path)
                    
                self.speak(f"Playing {song}")
            else:
                self.speak("No songs found")
                
        except Exception as e:
            self.speak("Sorry, I couldn't play music")
            print(f"Music error: {e}")

    def set_name(self):
        """Set assistant name"""
        self.speak("What would you like to call me?")
        name = self.listen_command()
        
        if name:
            try:
                with open("assistant_name.txt", "w") as file:
                    file.write(name.title())
                self.assistant_name = name.title()
                self.speak(f"Great! I'll be {self.assistant_name} from now on")
            except Exception as e:
                self.speak("Sorry, I couldn't save the name")
                print(f"Name save error: {e}")
        else:
            self.speak("I didn't catch that")

    def load_name(self):
        """Load assistant name from file"""
        try:
            with open("assistant_name.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Nova"  # Default name

    def search_wikipedia(self, query=None):
        """Search Wikipedia"""
        try:
            if not query or not query.strip():
                self.speak("What would you like to search on Wikipedia?")
                self.waiting_for_wikipedia_query = True
                return
                
            self.speak("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=2)
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError:
            self.speak("Multiple results found. Please be more specific")
        except wikipedia.exceptions.PageError:
            self.speak("No Wikipedia page found for that topic")
        except Exception as e:
            self.speak("Sorry, I couldn't search Wikipedia")
            print(f"Wikipedia error: {e}")

    def search_google(self, query=None):
        """Search Google with voice query"""
        try:
            if not query or not query.strip():
                self.speak("What would you like to search on Google?")
                self.waiting_for_google_query = True
                return
        
            # Format the search URL
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            wb.open(search_url)
            self.speak(f"Searching Google for {query}")
        
        except Exception as e:
            self.speak("Sorry, I couldn't search Google")
            print(f"Google search error: {e}")

    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
        except Exception as e:
            self.speak("Sorry, I couldn't get a joke right now")
            print(f"Joke error: {e}")

    def shutdown_system(self):
        """Shutdown the system"""
        self.speak("Shutting down the system. Goodbye!")
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['sudo', 'shutdown', '-h', 'now'])
            elif sys.platform.startswith('win'):
                os.system("shutdown /s /f /t 1")
        except Exception as e:
            self.speak("Sorry, I couldn't shutdown the system")
            print(f"Shutdown error: {e}")

    def restart_system(self):
        """Restart the system"""
        self.speak("Restarting the system. Please wait!")
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['sudo', 'reboot'])
            elif sys.platform.startswith('win'):
                os.system("shutdown /r /f /t 1")
        except Exception as e:
            self.speak("Sorry, I couldn't restart the system")
            print(f"Restart error: {e}")

    def process_command(self, query):
        """Process voice commands"""
        if not query:
            return True
    
        print(f"Processing command: '{query}'")
        print(f"Waiting for Wikipedia: {self.waiting_for_wikipedia_query}")
        print(f"Waiting for Google: {self.waiting_for_google_query}")
    
        # Handle follow-up queries
        if self.waiting_for_wikipedia_query:
            self.waiting_for_wikipedia_query = False
            self.search_wikipedia(query)
            return True
        
        if self.waiting_for_google_query:
            self.waiting_for_google_query = False
            self.search_google(query)
            return True
        
        # Time and date
        if "time" in query:
            self.get_time()
        
        elif "date" in query:
            self.get_date()
        
        # Wikipedia search
        elif "wikipedia" in query:
            search_query = query.replace("wikipedia", "").strip()
            self.search_wikipedia(search_query if search_query else None)
            
        # Google search
        elif "search google" in query or "google search" in query:
            search_query = query.replace("search google", "").replace("google search", "").strip()
            self.search_google(search_query if search_query else None)
            
        elif "search for" in query and ("google" in query or "on google" in query):
            search_query = query.replace("search for", "").replace("on google", "").replace("google", "").strip()
            self.search_google(search_query)
        
        elif "google" in query and any(word in query for word in ["search", "find", "look"]):
            search_query = query.replace("google", "").replace("search", "").replace("find", "").replace("look", "").strip()
            self.search_google(search_query)

        # Music
        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            self.play_music(song_name if song_name else None)
            
        # Web browsing
        elif "open youtube" in query:
            wb.open("https://youtube.com")
            self.speak("Opening YouTube")
            
        elif "open google" in query:
            wb.open("https://google.com")
            self.speak("Opening Google")
            
        # Assistant settings
        elif "change your name" in query or "change name" in query:
            self.set_name()
            
        # Screenshot - AUTOMATIC CAPTURE
        elif "screenshot" in query or "take screenshot" in query:
            self.take_screenshot()
            
        # Jokes
        elif "tell me a joke" in query or "joke" in query:
            self.tell_joke()
            
        # System control
        elif "shutdown" in query:
            self.shutdown_system()
            return False
            
        elif "restart" in query:
            self.restart_system()
            return False
            
        # Exit commands
        elif any(word in query for word in ["exit", "quit", "goodbye", "bye", "offline"]):
            self.speak("Goodbye! Have a great day!")
            return False
            
        else:
            self.speak("I'm not sure how to help with that. Try asking about time, date, Wikipedia, Google search, music, or jokes.")
            
        return True

    def run(self):
        """Main assistant loop"""
        try:
            self.greet_user()
            
            while True:
                try:
                    query = self.listen_command()
                    if not self.process_command(query):
                        break
                        
                except KeyboardInterrupt:
                    print("\nReceived interrupt signal...")
                    self.speak("Goodbye!")
                    break
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    self.speak("Sorry, something went wrong")
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
