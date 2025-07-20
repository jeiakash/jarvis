import webbrowser as wb
import urllib.parse

class EnhancedSearch:
    """Enhanced search functionality for the voice assistant"""
    
    def __init__(self, assistant):
        self.assistant = assistant
    
    def search_google(self, query=None):
        """Search Google with voice input"""
        if not query or not query.strip():
            self.assistant.speak("What would you like to search for?")
            query = self.assistant.listen_command()
            
        if query:
            try:
                # Encode the query for URL
                encoded_query = urllib.parse.quote_plus(query)
                search_url = f"https://www.google.com/search?q={encoded_query}"
                wb.open(search_url)
                self.assistant.speak(f"Searching Google for {query}")
            except Exception as e:
                self.assistant.speak("Sorry, I couldn't perform the Google search")
                print(f"Google search error: {e}")
        else:
            self.assistant.speak("I didn't catch what you wanted to search for")
    
    def search_youtube(self, query=None):
        """Search YouTube with voice input"""
        if not query or not query.strip():
            self.assistant.speak("What would you like to search on YouTube?")
            query = self.assistant.listen_command()
            
        if query:
            try:
                encoded_query = urllib.parse.quote_plus(query)
                search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
                wb.open(search_url)
                self.assistant.speak(f"Searching YouTube for {query}")
            except Exception as e:
                self.assistant.speak("Sorry, I couldn't search YouTube")
                print(f"YouTube search error: {e}")
        else:
            self.assistant.speak("I didn't catch what you wanted to search for")
    
    def search_amazon(self, query=None):
        """Search Amazon with voice input"""
        if not query or not query.strip():
            self.assistant.speak("What product would you like to search for on Amazon?")
            query = self.assistant.listen_command()
            
        if query:
            try:
                encoded_query = urllib.parse.quote_plus(query)
                search_url = f"https://www.amazon.com/s?k={encoded_query}"
                wb.open(search_url)
                self.assistant.speak(f"Searching Amazon for {query}")
            except Exception as e:
                self.assistant.speak("Sorry, I couldn't search Amazon")
                print(f"Amazon search error: {e}")
        else:
            self.assistant.speak("I didn't catch what you wanted to search for")
    
    def search_maps(self, query=None):
        """Search Google Maps with voice input"""
        if not query or not query.strip():
            self.assistant.speak("What location would you like to search for?")
            query = self.assistant.listen_command()
            
        if query:
            try:
                encoded_query = urllib.parse.quote_plus(query)
                search_url = f"https://www.google.com/maps/search/{encoded_query}"
                wb.open(search_url)
                self.assistant.speak(f"Searching maps for {query}")
            except Exception as e:
                self.assistant.speak("Sorry, I couldn't search maps")
                print(f"Maps search error: {e}")
        else:
            self.assistant.speak("I didn't catch the location you wanted to search for")
