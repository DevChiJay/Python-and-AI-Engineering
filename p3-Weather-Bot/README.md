# Weather Bot CLI 🌤️

A simple Python CLI application that demonstrates working with files and HTTP requests by fetching weather data and saving it to local files.

## Features

- 🌍 Fetch current weather data for any city
- 📄 Save weather data to JSON files
- 📊 Export weather data to CSV files
- 🔄 Mock data mode for learning without API key
- 💡 Beginner-friendly code with educational comments

## How It Works

This project teaches several important Python concepts:

1. **HTTP Requests**: Using the `requests` library to fetch data from web APIs
2. **JSON Parsing**: Converting JSON responses to Python dictionaries
3. **File Operations**: Reading from and writing to files (JSON and CSV)
4. **Error Handling**: Proper exception handling for network and file operations
5. **CLI Interaction**: Getting user input and providing feedback

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage (Mock Data)
```bash
python main.py
```

The application will run with mock data by default, which is perfect for learning and testing.

### Using Real Weather Data

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace `"demo_key"` in `main.py` with your actual API key
3. Run the application:
   ```bash
   python main.py
   ```

### Example Session
```
🌤️  Welcome to Weather Bot! 🌤️
This bot fetches weather data and saves it to files.
Data will be saved in the 'weather_data' directory.

Enter a city name (or 'quit' to exit): London
Using mock data (replace api_key with real one for live data)
Weather data fetched successfully!

==================================================
WEATHER REPORT FOR LONDON
==================================================
Temperature: 15.2°C
Feels like: 14.1°C
Humidity: 78%
Pressure: 1013 hPa
Weather: Clouds - few clouds
Wind Speed: 3.2 m/s
Visibility: 8500 meters
==================================================

Weather data saved to: weather_data/london_weather_20240915_143022.json

Export to CSV as well? (y/n): y
Weather data saved to CSV: weather_data/london_weather_20240915_143022.csv

✅ Weather data successfully saved!
```

## Project Structure

```
p3-Weather-Bot/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── weather_data/       # Directory created automatically for data files
    ├── city_weather_timestamp.json
    └── city_weather_timestamp.csv
```

## Learning Objectives

### File Operations
- Creating directories with `os.makedirs()`
- Writing JSON data with `json.dump()`
- Writing CSV data with `csv.DictWriter()`
- Using context managers (`with` statements) for safe file handling

### HTTP Requests
- Making GET requests with `requests.get()`
- Handling URL parameters
- Processing HTTP response codes
- Error handling for network operations

### JSON Processing
- Parsing JSON with `response.json()`
- Working with nested dictionaries
- Pretty-printing JSON with indentation

### Error Handling
- Using try/except blocks for different error types
- Handling network errors (`requests.exceptions.RequestException`)
- Handling JSON parsing errors (`json.JSONDecodeError`)
- File I/O error handling (`IOError`)

## Code Structure Explained

### WeatherBot Class
- `__init__()`: Sets up API configuration and creates data directory
- `fetch_weather()`: Makes HTTP request or returns mock data
- `save_to_json()`: Saves data as JSON file with timestamp
- `save_to_csv()`: Extracts and saves key data to CSV
- `display_weather()`: Shows formatted weather information
- `run()`: Main application loop with user interaction

### Key Python Concepts Demonstrated

1. **Class-based organization**: Code is organized in a class for better structure
2. **Type hints**: Function parameters and return types are annotated
3. **Error handling**: Multiple types of exceptions are caught and handled
4. **File path handling**: Using `os.path.join()` for cross-platform compatibility
5. **String formatting**: Various string formatting techniques
6. **Dictionary operations**: Extracting data from nested dictionaries with `.get()`

## Extending the Project

Try these modifications to learn more:

1. Add more weather data fields to the CSV export
2. Create a function to read and display saved weather data
3. Add weather data comparison between cities
4. Implement a weather history feature
5. Add data visualization with matplotlib
6. Create a web interface with Flask

## Notes

- The application creates timestamped files to avoid overwriting data
- Mock data is generated randomly for demonstration purposes
- Real API calls are limited (1000/month on free tier)
- All data is saved in the `weather_data` directory
