from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from compute import compute_tabulated, compute_LMS1
import numpy as np
import json

api = Flask(__name__)
CORS(api)

# Convert results and plots to JSON serializable format
def convert_to_json_serializable(data):
    # Convert numpy arrays to lists
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, np.ndarray):
                data[key] = value.tolist()
            elif isinstance(value, dict):
                convert_to_json_serializable(value)
    # Lists that might contain numpy arrays
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, np.ndarray):
                data[i] = item.tolist()
            elif isinstance(item, dict):
                convert_to_json_serializable(item)

@api.route('/')
def home():
    endpoints_description = """
Welcome to the CIE colour match API. Use the endpoints listed below to interact with the API.

Endpoints:

1. Path: /compute_all_specific_data
   Method: POST
   Description: Computes specific visual data based on the provided parameters (field_size, age, min, max, step). Returns both results and plots.

2. Path: /compute_all_default_data
   Method: GET
   Description: Computes default visual data for all color functions. Returns both results and plots.

3. Path: /compute_LMS_default_data
   Method: GET
   Description: Computes default visual data specifically for the LMS color function. Returns both results and plots.

4. Path: /compute_LMS_plots_default_data
   Method: GET
   Description: Computes default visual data specifically for the LMS color function. Returns only plots.

5. Path: /compute_LMS_results_default_data
   Method: GET
   Description: Computes default visual data specifically for the LMS color function. Returns only results.
    """
    response = make_response(endpoints_description, 200)
    response.mimetype = "text/plain"
    return response




class VisualDataAPI:
    def __init__(self):
        pass


# Computes the default tabulated data
    def compute_default(self):
        """
        This function computes the plots and table results for 
        for all the colour functions. 
        This funciton calaculates the results based on the default values.
        Change what is computed by changing the invoced to function in this line:
        results, plots = compute_LMS1(field_size, age, λ_min, λ_max, λ_step)
        """
        field_size, age, λ_min, λ_max, λ_step = 2.0, 32, 390.0, 830.0, 1.0
        # N.B! Change the invoced to function to compute_tabulated
        results, plots = compute_LMS1(field_size, age, λ_min, λ_max, λ_step)
        convert_to_json_serializable(results)
        convert_to_json_serializable(plots)
        return results, plots

# Computes the tabulated data
    def compute(self, data):
        """
        This function computes the plots and table results for 
        for all the colour functions. 
        This funciton calaculates the results based parameters specified by the user.
        Change what is computed by changing the invoced to function in this line:
        results, plots = compute_LMS1(field_size, age, λ_min, λ_max, λ_step)
        """
        field_size = float(data.get('field_size', 0))
        age = float(data.get('age', 0))
        λ_min = float(data.get('min', 390))
        λ_max = float(data.get('max', 830))
        λ_step = float(data.get('step', 1))
        # N.B! Change the invoced to function to compute_tabulated
        results, plots = compute_LMS1(field_size, age, λ_min, λ_max, λ_step)
        convert_to_json_serializable(results)
        convert_to_json_serializable(plots)
        return results, plots



# Endpoint that computes and return all the specific data
@api.route('/compute_all_specific_data', methods=['POST'])
def compute_all_specific_data():
    data_api = VisualDataAPI()
    data = request.json
    results, plots = data_api.compute(data)
    
    return jsonify({'results': results, 'plots': plots})

# Endpoint that computes and retruns all the default data
@api.route('/compute_all_default_data', methods=['GET'])
def compute_all_default_data():
    data_api = VisualDataAPI()
    results, plots = data_api.compute_default()
    
    return jsonify({'results': results, 'plots': plots})

# Endpoint that computes all data and filters it to the LMS color function
# Retruns both results and plots
@api.route('/compute_LMS_default_data', methods=['GET'])
def compute_LMS_default_data():
    data_api = VisualDataAPI()
    results, plots = data_api.compute_default()
    lms_data = {
        'results': results.get('LMS', []),
        'plots': plots.get('LMS', [])
    }
    return jsonify(lms_data)

# Endpoint that computes all data and filters it to the LMS color function
# Retruns onlyplots
@api.route('/compute_LMS_plots_default_data', methods=['GET'])
def compute_LMS_plots_default_data():
    data_api = VisualDataAPI()
    _, plots = data_api.compute_default()
    lms_plots = plots.get('LMS', [])
    return jsonify({'plots': lms_plots})


# Endpoint that computes all data and filters it to the LMS color function
# Retruns results
@api.route('/compute_LMS_results_default_data', methods=['GET'])
def compute_LMS_results_default_data():
    data_api = VisualDataAPI()
    results, _ = data_api.compute_default()
    lms_results = results.get('LMS', [])
    return jsonify({'results': lms_results})

@api.route('/LMS_results', methods=['GET'])
def LMS_results():
    file_path = 'lms_default_data.json'
    
    # Open and load the JSON file
    with open(file_path, 'r') as file:
        lms_results = json.load(file)
    lms_plots = lms_results.get('results', [])
    # Return the LMS results in the response
    return jsonify({'results': lms_plots})

@api.route('/LMS_plots', methods=['GET'])
def LMS_plots():
    file_path = 'lms_default_data.json'
    
    # Open and load the JSON file
    with open(file_path, 'r') as file:
        lms_plots = json.load(file)
    lms_pl = lms_plots.get('plots', [])
    # Return the LMS results in the response
    return jsonify({'plots': lms_pl})


if __name__ == '__main__':
    api.run(debug=True)


     
     
"""   
========================================
===============JSON BODY================
   {
    "field_size": 1,
    "age": 99,
    "min": 390,
    "max": 830,
    "step": 1,
    "type": "specific_computation"
   }

==================Header=================
   key: content-type
   value: application/json
"""