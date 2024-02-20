


import cieapi
from cieapi import VisualDataAPI
from cieapi import compute_all_default_data
import requests
import pprint

# Function that retrieves all plot points and result points for a specified color function.
def get_color_function_data(json_data, color_function):
    data = {
        'plots': [],
        'results': []
    }

    # Checks if the color function exists in plots and retrieves its data
    if color_function in json_data['plots']:
        data['plots'] = json_data['plots'][color_function]

    # Checks if the color function exists in results and retrieves its data
    if color_function in json_data['results']:
        data['results'] = json_data['results'][color_function]

    return data


# Function that makes a GET request to the api 
# to retrieve the data for a specified color function
def simulate_api_call_and_process_data(color_function):
    # The endpoint
    url = 'http://127.0.0.1:5000/compute_all_default_data'
    
    # Make the GET request to the Flask application
    response = requests.get(url)
    
    # Error handling
    if response.status_code == 200:
        json_data = response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}
    
    # Process the JSON data to get information for only the specified color function
    color_function_data = get_color_function_data(json_data, color_function)
    
    return color_function_data



# Usage
# Specify the color function we want data for
color_function = 'LMS'  
data = simulate_api_call_and_process_data(color_function)

# Print the data for testing purposes
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)