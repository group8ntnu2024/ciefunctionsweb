from flask import Flask, request, jsonify

app = Flask(__name__)

class VisualDataAPI:
    def __init__(self):
        self.computation = VisualDataComputation()
    
    def compute_visual_data(self, data):
        # Use self.computation methods to compute and return results
        # Example: result = self.computation.chop(data)
        # return result

@api.route('/compute_visual_data', methods=['POST'])
def compute_visual_data_endpoint():
    data_api = VisualDataAPI()
    data = request.json
    # Extract necessary inputs from data
    field_size = data.get('field_size')
    age = data.get('age')
    # Add more parameters as needed

    # Call the compute method and return its result
    result = data_api.compute_visual_data(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)