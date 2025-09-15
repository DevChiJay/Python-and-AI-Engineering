#!/usr/bin/env python3
"""
Weather Bot Demo Script
Demonstrates how to use the WeatherBot class programmatically.
"""

from main import WeatherBot


def demo_weather_bot():
    """Demonstrate the Weather Bot functionality."""
    print("🔬 Weather Bot Demo Script")
    print("=" * 40)
    
    # Create a WeatherBot instance
    bot = WeatherBot()
    
    # List of cities to demonstrate
    demo_cities = ["Paris", "Tokyo", "New York", "Sydney"]
    
    for city in demo_cities:
        print(f"\n📍 Processing: {city}")
        print("-" * 30)
        
        # Fetch weather data
        weather_data = bot.fetch_weather(city)
        
        if weather_data:
            # Display the weather
            bot.display_weather(weather_data)
            
            # Save to JSON
            json_file = bot.save_to_json(weather_data, city)
            
            # Save to CSV
            csv_file = bot.save_to_csv(weather_data, city)
            
            print(f"✅ Data saved for {city}")
        else:
            print(f"❌ Failed to get data for {city}")
        
        print("\n" + "=" * 50)
    
    print("\n🎉 Demo completed! Check the 'weather_data' directory for saved files.")


if __name__ == "__main__":
    demo_weather_bot()
