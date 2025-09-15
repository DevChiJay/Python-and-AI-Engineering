#!/usr/bin/env python3
"""
Weather Bot CLI Application
A simple CLI tool to fetch weather data and save it to files.
"""

import requests
import json
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any, Optional


class WeatherBot:
    """A simple weather bot that fetches weather data and saves it to files."""
    
    def __init__(self):
        # OpenWeatherMap API (free tier allows 1000 calls/month)
        # You can get a free API key at: https://openweathermap.org/api
        load_dotenv()

        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')  # Replace with your actual API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Create data directory if it doesn't exist
        self.data_dir = "weather_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created directory: {self.data_dir}")
    
    def fetch_weather(self, city: str) -> Optional[Dict[Any, Any]]:
        """
        Fetch weather data from API or return mock data if API key is demo.
        
        Args:
            city (str): Name of the city to get weather for
            
        Returns:
            Dict: Weather data or None if request fails
        """
        if self.api_key == "demo_key":
            # Return mock data for demonstration
            print("Using mock data (replace api_key with real one for live data)")
            return self._get_mock_weather(city)
        
        try:
            # Build the API request URL with parameters
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            print(f"Fetching weather data for {city}...")
            
            # Make HTTP GET request to the weather API
            response = requests.get(self.base_url, params=params)
            
            # Check if request was successful (status code 200)
            if response.status_code == 200:
                # Parse JSON response into Python dictionary
                weather_data = response.json()
                print("Weather data fetched successfully!")
                return weather_data
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
    
    def _get_mock_weather(self, city: str) -> Dict[Any, Any]:
        """Generate mock weather data for demonstration purposes."""
        import random
        
        # Mock weather data structure similar to OpenWeatherMap API
        mock_data = {
            "coord": {"lon": random.uniform(-180, 180), "lat": random.uniform(-90, 90)},
            "weather": [
                {
                    "id": 800,
                    "main": random.choice(["Clear", "Clouds", "Rain", "Snow"]),
                    "description": random.choice(["clear sky", "few clouds", "light rain", "snow"]),
                    "icon": "01d"
                }
            ],
            "base": "stations",
            "main": {
                "temp": round(random.uniform(-10, 35), 1),
                "feels_like": round(random.uniform(-10, 35), 1),
                "temp_min": round(random.uniform(-15, 30), 1),
                "temp_max": round(random.uniform(-5, 40), 1),
                "pressure": random.randint(950, 1050),
                "humidity": random.randint(20, 90)
            },
            "visibility": random.randint(1000, 10000),
            "wind": {
                "speed": round(random.uniform(0, 20), 1),
                "deg": random.randint(0, 360)
            },
            "clouds": {"all": random.randint(0, 100)},
            "dt": int(datetime.now().timestamp()),
            "sys": {
                "type": 1,
                "id": 1234,
                "country": "XX",
                "sunrise": int(datetime.now().timestamp()) - 3600,
                "sunset": int(datetime.now().timestamp()) + 3600
            },
            "timezone": 0,
            "id": 123456,
            "name": city.title(),
            "cod": 200
        }
        return mock_data
    
    def save_to_json(self, weather_data: Dict[Any, Any], city: str) -> str:
        """
        Save weather data to a JSON file.
        
        Args:
            weather_data (Dict): Weather data to save
            city (str): City name for filename
            
        Returns:
            str: Path to the saved file
        """
        # Create filename with timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{city.lower().replace(' ', '_')}_weather_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Open file in write mode and save JSON data
            with open(filepath, 'w', encoding='utf-8') as json_file:
                # Convert Python dict to JSON string with pretty formatting
                json.dump(weather_data, json_file, indent=2, ensure_ascii=False)
            
            print(f"Weather data saved to: {filepath}")
            return filepath
            
        except IOError as e:
            print(f"Error saving JSON file: {e}")
            return ""
    
    def save_to_csv(self, weather_data: Dict[Any, Any], city: str) -> str:
        """
        Save weather data to a CSV file.
        
        Args:
            weather_data (Dict): Weather data to save
            city (str): City name for filename
            
        Returns:
            str: Path to the saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{city.lower().replace(' ', '_')}_weather_{timestamp}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Extract relevant data for CSV format
            main_data = weather_data.get('main', {})
            weather_info = weather_data.get('weather', [{}])[0]
            wind_data = weather_data.get('wind', {})
            
            # Define CSV headers and corresponding data
            csv_data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'city': weather_data.get('name', city),
                'country': weather_data.get('sys', {}).get('country', 'N/A'),
                'temperature_celsius': main_data.get('temp', 'N/A'),
                'feels_like_celsius': main_data.get('feels_like', 'N/A'),
                'humidity_percent': main_data.get('humidity', 'N/A'),
                'pressure_hpa': main_data.get('pressure', 'N/A'),
                'weather_main': weather_info.get('main', 'N/A'),
                'weather_description': weather_info.get('description', 'N/A'),
                'wind_speed_mps': wind_data.get('speed', 'N/A'),
                'visibility_meters': weather_data.get('visibility', 'N/A')
            }
            
            # Write data to CSV file
            with open(filepath, 'w', newline='', encoding='utf-8') as csv_file:
                # Create CSV writer with headers
                writer = csv.DictWriter(csv_file, fieldnames=csv_data.keys())
                
                # Write header row
                writer.writeheader()
                
                # Write data row
                writer.writerow(csv_data)
            
            print(f"Weather data saved to CSV: {filepath}")
            return filepath
            
        except IOError as e:
            print(f"Error saving CSV file: {e}")
            return ""
    
    def display_weather(self, weather_data: Dict[Any, Any]) -> None:
        """Display weather information in a user-friendly format."""
        if not weather_data:
            print("No weather data to display.")
            return
        
        # Extract data from the nested dictionary structure
        main_data = weather_data.get('main', {})
        weather_info = weather_data.get('weather', [{}])[0]
        wind_data = weather_data.get('wind', {})
        
        print("\n" + "="*50)
        print(f"WEATHER REPORT FOR {weather_data.get('name', 'Unknown').upper()}")
        print("="*50)
        print(f"Temperature: {main_data.get('temp', 'N/A')}°C")
        print(f"Feels like: {main_data.get('feels_like', 'N/A')}°C")
        print(f"Humidity: {main_data.get('humidity', 'N/A')}%")
        print(f"Pressure: {main_data.get('pressure', 'N/A')} hPa")
        print(f"Weather: {weather_info.get('main', 'N/A')} - {weather_info.get('description', 'N/A')}")
        print(f"Wind Speed: {wind_data.get('speed', 'N/A')} m/s")
        print(f"Visibility: {weather_data.get('visibility', 'N/A')} meters")
        print("="*50)
    
    def run(self) -> None:
        """Main method to run the weather bot."""
        print("🌤️  Welcome to Weather Bot! 🌤️")
        print("This bot fetches weather data and saves it to files.")
        print(f"Data will be saved in the '{self.data_dir}' directory.")
        print()
        
        while True:
            try:
                # Get city name from user input
                city = input("Enter a city name (or 'quit' to exit): ").strip()
                
                if city.lower() in ['quit', 'exit', 'q']:
                    print("Thank you for using Weather Bot! 👋")
                    break
                
                if not city:
                    print("Please enter a valid city name.")
                    continue
                
                # Fetch weather data from API
                weather_data = self.fetch_weather(city)
                
                if weather_data:
                    # Display weather information
                    self.display_weather(weather_data)
                    
                    # Save to JSON file
                    json_path = self.save_to_json(weather_data, city)
                    
                    # Ask if user wants CSV export too
                    export_csv = input("\nExport to CSV as well? (y/n): ").strip().lower()
                    if export_csv in ['y', 'yes']:
                        csv_path = self.save_to_csv(weather_data, city)
                    
                    print(f"\n✅ Weather data successfully saved!")
                else:
                    print("❌ Failed to fetch weather data. Please try again.")
                
                print("\n" + "-"*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled. Goodbye! 👋")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


def main():
    """Entry point of the application."""
    # Create and run the weather bot
    bot = WeatherBot()
    bot.run()


# This block ensures the script only runs when executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()