from flask import Flask, request, jsonify
from compute import compute_tabulated
api = Flask(__name__)

class VisualDataAPI:
    def __init__(self):
        pass
    
    def compute_visual_data(self, data):
        if 'type' in data and data['type'] == 'specific_computation':
            result = self.compute_tabulated(data)
        else:
            result = self.compute_default_tabulated(data)
        return result
    
    
    def compute_tabulated(self, data):
        return {'status': 'success', 'message': 'Computation not implemented yet'}
    
    def compute_default_tabulated(self, data):
        return {'status': 'success', 'message': 'Deafult computation not implemented yet'}
    







@api.route('/compute_default_visual_data', methods=['POST'])
def compute_default_visual_data_endpoint():
    data_api = VisualDataAPI()
    data = {'type': 'default_computation'}
    result = data_api.compute_visual_data(data)
    return jsonify(result)

@api.route('/compute_specific_visual_data', methods=['POST'])
def compute_specific_visual_data_endpoint():
    data_api = VisualDataAPI()
    data = request.json
    data['type'] = 'specific_computation'
    result = data_api.compute_visual_data(data)
    return jsonify(result)

if __name__ == '__main__':
    api.run(debug=True)
