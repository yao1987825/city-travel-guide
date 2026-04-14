import re

class AutoTrigger:
    def __init__(self):
        self.city_scripts = {
            'weather': self.get_weather,
            'itinerary': self.get_itinerary,
            'images': self.get_images,
            'food': self.get_food,
            'pitfalls': self.get_pitfalls
        }

    def trigger_script(self, user_input):
        # Detect city names and parameters from user input
        city_name = self.extract_city_name(user_input)
        intent_type = self.detect_intent(user_input)
        
        if city_name and intent_type:
            script_function = self.city_scripts.get(intent_type)
            if script_function:
                return script_function(city_name)
            else:
                return "No matching script found."
        return "Could not detect city or intent."

    def extract_city_name(self, user_input):
        # Dummy implementation: improve with a better NLP model
        match = re.search(r'in (\w+)', user_input)
        return match.group(1) if match else None

    def detect_intent(self, user_input):
        # Simple keyword-based intent detection
        if 'weather' in user_input:
            return 'weather'
        elif 'itinerary' in user_input:
            return 'itinerary'
        elif 'images' in user_input:
            return 'images'
        elif 'food' in user_input:
            return 'food'
        elif 'pitfalls' in user_input:
            return 'pitfalls'
        return None

    def get_weather(self, city_name):
        return f'Fetching weather for {city_name}'

    def get_itinerary(self, city_name):
        return f'Generating itinerary for {city_name}'

    def get_images(self, city_name):
        return f'Fetching images for {city_name}'

    def get_food(self, city_name):
        return f'Finding food spots in {city_name}'

    def get_pitfalls(self, city_name):
        return f'Highlighting pitfalls in {city_name}'

# Example usage:
# auto_trigger = AutoTrigger()
# response = auto_trigger.trigger_script('Show me the weather in Paris')

