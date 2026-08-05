#!/usr/bin/env python3
"""
Weather Bot Extensions
Examples of how to extend the basic Weather Bot functionality.
"""

import json
import os
from datetime import datetime
from main import WeatherBot


class ExtendedWeatherBot(WeatherBot):
    """Extended version of WeatherBot with additional features."""
    
    def read_saved_weather(self, city: str) -> list:
        """
        Read all saved weather data for a specific city.
        
        Args:
            city (str): City name to search for
            
        Returns:
            list: List of weather data dictionaries
        """
        city_pattern = city.lower().replace(' ', '_')
        weather_files = []
        
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            print(f"No data directory found: {self.data_dir}")
            return []
        
        # Find all JSON files for the specified city
        for filename in os.listdir(self.data_dir):
            if filename.startswith(city_pattern) and filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        weather_data = json.load(file)
                        weather_files.append({
                            'filename': filename,
                            'data': weather_data
                        })
                except (IOError, json.JSONDecodeError) as e:
                    print(f"Error reading {filename}: {e}")
        
        return weather_files
    
    def compare_cities(self, cities: list) -> None:
        """
        Compare weather between multiple cities.
        
        Args:
            cities (list): List of city names to compare
        """
        print("\n🌍 Weather Comparison")
        print("=" * 60)
        
        city_data = {}
        
        # Fetch weather for all cities
        for city in cities:
            weather_data = self.fetch_weather(city)
            if weather_data:
                city_data[city] = weather_data
        
        if not city_data:
            print("No weather data available for comparison.")
            return
        
        # Display comparison table
        print(f"{'City':<15} {'Temp (°C)':<10} {'Humidity':<10} {'Weather':<20}")
        print("-" * 60)
        
        for city, data in city_data.items():
            main_data = data.get('main', {})
            weather_info = data.get('weather', [{}])[0]
            
            temp = main_data.get('temp', 'N/A')
            humidity = main_data.get('humidity', 'N/A')
            weather = weather_info.get('main', 'N/A')
            
            print(f"{city:<15} {temp:<10} {humidity}%{'':<7} {weather:<20}")
    
    def weather_history(self, city: str) -> None:
        """
        Display weather history for a city.
        
        Args:
            city (str): City name to show history for
        """
        weather_files = self.read_saved_weather(city)
        
        if not weather_files:
            print(f"No weather history found for {city}")
            return
        
        print(f"\n📊 Weather History for {city.title()}")
        print("=" * 50)
        
        # Sort by filename (which contains timestamp)
        weather_files.sort(key=lambda x: x['filename'])
        
        for entry in weather_files:
            data = entry['data']
            main_data = data.get('main', {})
            weather_info = data.get('weather', [{}])[0]
            
            # Extract timestamp from filename
            filename = entry['filename']
            timestamp_part = filename.split('_')[-2] + '_' + filename.split('_')[-1].replace('.json', '')
            
            print(f"📅 {timestamp_part}")
            print(f"   Temperature: {main_data.get('temp', 'N/A')}°C")
            print(f"   Weather: {weather_info.get('main', 'N/A')}")
            print()


def demo_extensions():
    """Demonstrate the extended functionality."""
    print("🚀 Weather Bot Extensions Demo")
    print("=" * 40)
    
    # Create extended bot
    bot = ExtendedWeatherBot()
    
    # Demo 1: Compare multiple cities
    print("\n1. Comparing multiple cities:")
    bot.compare_cities(["London", "Paris", "Berlin", "Madrid"])
    
    # Demo 2: Show weather history (if any exists)
    print("\n2. Weather history example:")
    bot.weather_history("Paris")
    
    print("\n✨ Extensions demo completed!")


if __name__ == "__main__":
    demo_extensions()
