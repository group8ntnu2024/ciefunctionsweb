from flask import Flask, request, jsonify
from compute import compute_tabulated  # Import the compute_tabulated function from compute.py

api = Flask(__name__)

class VisualDataAPI:
    def __init__(self):
        pass

# Checks the type of claculation to be performed
    def compute_visual_data(self, data):
        if 'type' in data and data['type'] == 'specific_computation':
            result = self.compute_tabulated(data)
        else:
            result = self.compute_default_tabulated(data)
        return result

# Computes the default tabulated data
    def compute_default_tabulated(self, data=None):
        field_size = 0
        age = 0
        λ_min = 390
        λ_max = 830
        λ_step = 1
        
        #removed for testing purposes
        #return compute_tabulated(field_size, age, λ_min, λ_max, λ_step)
        return age + λ_min + λ_max

# Computes the tabulated data
    def compute_tabulated(self, data):
        field_size = int(data.get('field_size', 0))
        age = int(data.get('age', 0))
        λ_min = int(data.get('min', 390))
        λ_max = int(data.get('max', 830))
        λ_step = int(data.get('step', 1))

        #removed for testing purposes
        #return compute_tabulated(field_size, age, λ_min, λ_max, λ_step)
        return age + λ_min + λ_max



# Endpoint to compute the specific data
@api.route('/compute_visual_data', methods=['POST'])
def compute_visual_data_endpoint():
    data_api = VisualDataAPI()
    data = request.json
    result = data_api.compute_visual_data(data)
    return jsonify(result)

# Endpoint to compute the default data
@api.route('/compute_default_visual_data', methods=['GET'])
def compute_default_visual_data_endpoint():
    data_api = VisualDataAPI()
    result = data_api.compute_default_tabulated()
    return jsonify(result)

if __name__ == '__main__':
    api.run(debug=True)
