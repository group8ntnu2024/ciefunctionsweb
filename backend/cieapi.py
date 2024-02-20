from flask import Flask, request, jsonify
from compute import compute_tabulated
import numpy as np

api = Flask(__name__)

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





class VisualDataAPI:
    def __init__(self):
        pass

# Checks the type of claculation to be performed
    def compute_visual_data(self, data):
        if 'type' in data and data['type'] == 'specific_computation':
            results, plots = self.compute(data)
        # Can be removed without affecting functionality of the API.
        # Default computations should be gotten
        # with the get request /compute_default_visual_data
        # Keeping it in case of future changes
        elif 'type' in data and data['type'] == 'default_computation':
            results, plots = self.compute_default()
        else:
            results, plots = {"error": "Invalid computation type specified."}, {}            
        return results, plots

# Computes the default tabulated data
    def compute_default(self):
        field_size, age, λ_min, λ_max, λ_step = 0, 0, 390, 830, 1
        results, plots = compute_tabulated(field_size, age, λ_min, λ_max, λ_step)
        convert_to_json_serializable(results)
        convert_to_json_serializable(plots)
        return results, plots

# Computes the tabulated data
    def compute(self, data):
        field_size = float(data.get('field_size', 0))
        age = float(data.get('age', 0))
        λ_min = float(data.get('min', 390))
        λ_max = float(data.get('max', 830))
        λ_step = float(data.get('step', 1))
        results, plots = compute_tabulated(field_size, age, λ_min, λ_max, λ_step)
        convert_to_json_serializable(results)
        convert_to_json_serializable(plots)
        return results, plots



# Endpoint to compute the specific data
@api.route('/compute_visual_data', methods=['POST'])
def compute_visual_data_endpoint():
    data_api = VisualDataAPI()
    data = request.json
    results, plots = data_api.compute_visual_data(data)
    
    #Check if error occurred
    if 'error' in results:
        return jsonify(results, "Error 400 Bad request")
    
    return jsonify({'results': results, 'plots': plots})

# Endpoint to compute the default data
@api.route('/compute_default_visual_data', methods=['GET'])
def compute_default_visual_data_endpoint():
    data_api = VisualDataAPI()
    results, plots = data_api.compute_default()
    return jsonify({'results': results, 'plots': plots})

if __name__ == '__main__':
    api.run(debug=True)



#========================================
#===============JSON BODY================
#   {
#    "field_size": 1,
#    "age": 99,
#    "min": 390,
#    "max": 830,
#    "step": 1,
#    "type": "specific_computation"
#   }
#
#
#==================Header=================
#   key: content-type
#   value: application/json