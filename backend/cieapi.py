import requests
from flask import Flask, request, jsonify, make_response, Response
from flask_cors import CORS
from pandas._testing import assert_frame_equal

from compute import compute_tabulated, compute_LMS1, my_round, compute_LMS, LMS_energy, chop,\
    Vλ_energy_and_LM_weights, compute_MacLeod_Boynton_diagram, compute_Maxwellian_diagram
import scipy.interpolate
import numpy as np
import pandas as pd
import json
from decimal import Decimal
from array import array
import base64
import sqlite3

from computemodularization import compute_MacLeod_Modular, compute_Maxwellian_Modular, compute_LMS_Modular

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

-   CIE LMS cone fundamentals with optional logarithmic values and 9 significant figures

    Path: /LMS
    Method: GET
    Parameters:
        'mode': Either 'plot' or 'result' for the type of return
        'field_size': A float number for the field size wished
        'age': An integer detailing the age wished for computation
        'min': Minimum value of domain
        'max': Maximum value of domain
        'step_size': The size of steps for each computation
        'log10': Optional with no value needed; gives logarithmic values of function
        'base': Optional with no value needed; gives 9 significant figures
    Examples:
        /LMS?mode=result&field_size=2.0&age=32&min=390.0&max=830.0&step-size=1.0
        /LMS?mode=plot&field_size=2.0&age=19&min=390.0&max=830.0&step-size=1.0&log10
        /LMS?mode=result&field_size=3.0&age=56&min=390.0&max=810.0&step-size=1.0&base

-   MacLeod-Boynton ls chromaticity diagram

    Path: /LMS-MB
    Method: GET
    Parameters:
        'mode': Either 'plot' or 'result' for the type of return
        'field_size': A float number for the field size wished
        'age': An integer detailing the age wished for computation
        'min': Minimum value of domain
        'max': Maximum value of domain
        'step_size': The size of steps for each computation
        'norm': Optional with no value needed; gives normalization coefficients
        'white': Optional with no value needed; gives values for Illuminant E
        'purple': Optional with no value needed; gives values for purple line's point of tangency with spectrum locus
        The optional parameters above cannot be used with each other, and will result in an Error Response.
    Examples:
        /LMS-MB?mode=result&field_size=2.0&age=32&min=390.0&max=830.0&step-size=1.0
        /LMS-MB?mode=plot&field_size=2.0&age=19&min=390.0&max=830.0&step-size=1.0
        /LMS-MB?mode=result&field_size=2.0&age=32&min=390.0&max=830.0&step-size=1.0&norm

-   Maxwellian lm chromacity diagram
    Path: /LMS-MW
    Method: GET
    Parameters:
        'mode': Either 'plot' or 'result' for the type of return
        'field_size': A float number for the field size wished
        'age': An integer detailing the age wished for computation
        'min': Minimum value of domain
        'max': Maximum value of domain
        'step_size': The size of steps for each computation
        'norm': Optional with no value needed; gives normalization coefficients
        'white': Optional with no value needed; gives values for Illuminant E
        'purple': Optional with no value needed; gives values for purple line's point of tangency with spectrum locus
        The optional parameters above cannot be used with each other, and will result in an Error Response.
    Examples:
        /LMS-MW?mode=result&field_size=2.0&age=12&min=390.0&max=830.0&step-size=1.0&norm
        /LMS-MW?mode=plot&field_size=2.0&age=12&min=390.0&max=830.0&step-size=1.0
    
Note: Endpoints may display floating point error for wavelengths when having mode=plot. Other than that,
it should display every correctly on mode=result. This will of course be fixed in the future.

-   Testing Endpoint
    Path: /testing
    Method: GET
    Parameters:
        NONE
    Note: 
        This is a developmental testing endpoint, used temporarily in development alongside debugging tools to ensure:
        1. That each endpoint calculates the right values given parameters.
        2. That each endpoint dispenses/outputs these values correctly and exactly as intended.
        It will return a Boolean value for each endpoint, indicating if it has managed to fulfill both of these goals.


 ------- OLD API DOCUMENTATION ----------
 

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

def wrapperDictionary(calculation, parameters):

    """
    wrapperDictionary is a higher-order function that retrieves the result from calculation given parameters,
    and packages it in a DataFrame (to make it resistant to floating point errors), before it is then
    made into a JSON string and returned.
    In addition, it also sets the pandas settings to have higher precision, as pandas tends to round down
    any floating values over a specific limit - these settings ensure that this doesn't happen, and that the
    data is untampered.

    Parameters
    ----------
    calculation: An endpoint's modularized compute function (from computemodularization.py).
    parameters: A dictionary representing the URL parameters.

    Returns
    -------
    A JSON string from a DataFrame with the results from the modularized compute function 'calculation',
    given the parameters of 'parameters'.

    """

    # a problem the Pandas DataFrames sometimes have is that their DataFrames cannot support
    # something over a given specific precision (and rounds it down, creating wrong results in endpoints)
    # the following options fixes that problem
    pd.set_option("display.precision", 12)
    pd.set_option("styler.format.precision", 12)
    dataframe = pd.DataFrame(calculation(parameters)).to_json(orient="values", double_precision=15)
    return dataframe

"""
    The endpoints for the API. 
    
    All of these functions are near identical, with the only exception being what calculation
    function they pass onto wrapperDictionary. Other than that, they're all endpoint functions for each
    respective endpoint.
"""

@api.route('/LMS', methods=['GET'])
def LMS():
    parameterCheck = createAndCheckParameters(True)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        wrapperDictionary(compute_LMS_Modular,
                          createAndCheckParameters(True)),
        mimetype='application/json')

@api.route('/LMS-MB', methods=['GET'])
def MB():
    parameterCheck = createAndCheckParameters(True)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        wrapperDictionary(compute_MacLeod_Modular,
                          createAndCheckParameters(True)),
        mimetype='application/json')

@api.route('/LMS-MW', methods=['GET'])
def maxwellian():
        parameterCheck = createAndCheckParameters(True)
        # parameterCheck may either be a dictionary (which means that all parameters are alright),
        # or a Response object (which means that a mandatory parameter is not filled, so calculations
        # cannot proceed further).
        if isinstance(parameterCheck, Response):
            return parameterCheck

        return Response(
            wrapperDictionary(compute_Maxwellian_Modular,
                              createAndCheckParameters(True)),
                                mimetype='application/json')

def createAndCheckParameters(disabled):

    """

    Parameters
    ----------
    disabled: A boolean which will enable/disable the checking of most parameters except for field_size
    (which is necessary for CIE XYZ std colour-matching funcs and CIE xy std cromaticity diagram).

    Returns
    -------
    Either:
        - A dictionary called 'parameter' with all URL parameters collected properly.
        - A Response object with client-error HTTP status codes, representing a client's faulty
        URL input/parameters.

    """
    def checkArgument(arga, theirType):
        # a try-except clause to stop potential other errors that may arise from parameters
        try:
            if request.args.get(arga) is None:
                error_message = "ERROR: Value of parameter " + arga + " is not filled."
                return Response(error_message, status=400)
            else:
                return theirType(request.args.get(arga))
        except:
            return Response("ERROR: Mandatory parameter " + arga + " not present.", status=400)

    """
        checkArgument is a simple small internal higher-order function that simply checks if a mandatory
        parameter is present - and if it is, returns the value with the given expected type of value. Else,
        it returns the Response error object.
    """

    # uses checkArgument to fill in all mandatory parameters
    parameters = {
        # mostly mandatory parameters
        "field_size": checkArgument('field_size', float),
        "mode": checkArgument('mode', str),
        "age": checkArgument('age', int),
        "λ_min": checkArgument('min', float),
        "λ_max": checkArgument('max', float),
        "λ_step": checkArgument('step-size', float),
    }

    # goes through all of the mandatory parameters; if any of them are a Response object,
    # that means at least one of the values aren't filled in properly, so the parameters
    # cannot be used - hence, the return of Response with error status code
    for value in parameters.values():
        if isinstance(value, Response):
            return value

    # Doing mandatory parameter-specific error handling
    if parameters['field_size'] > 10 or parameters['field_size'] < 1:
        return Response("ERROR: Invalid field size. Please input a value of degree between 1.0 and 10.0.", status=400)
    if parameters['mode'] not in ['plot', 'result']:
        return Response("ERROR: Parameter 'mode' is not properly set. Please use either 'plot' or 'result'.", status=400)
    if parameters['age'] <= 0 or parameters['age'] > 99:
        return Response("ERROR: Parameter 'age' is invalid; please input values between 1-99.", status=400)
    if parameters['λ_min'] >= parameters['λ_max']:
        return Response("ERROR: Invalid nm values for min and max domain; min cannot be lower than max.", status=400)
    if parameters['λ_min'] < 390:
        return Response("ERROR: Minimum domain cannot be lower than 390 nm. "
                        "Please change the value input.", status=400)
    if parameters['λ_max'] > 830:
        return Response("ERROR: Maximum domain cannot be higher than 830 nm. "
                        "Please change the max domain input. ", status=400)
    if parameters['λ_step'] > 5 or parameters['λ_step'] < 0.1:
        return Response("ERROR: Invalid step size. Please input a value of nm between 0.1 and 5.0.", status=400)

    # Now, adding optional/specific parameters
    parameters['log'] = True if request.args.get('log10') is not None else False
    parameters['base'] = True if request.args.get('base') is not None else False
    parameters['white'] = True if request.args.get('white') is not None else False
    parameters['purple'] = True if request.args.get('purple') is not None else False

    if parameters['purple'] and parameters['white']:
        return Response("ERROR: Cannot have purple line points of tangency activated as parameter alongside"
                        " actviated parameter for Illuminant E. Please deactivate one of them.", status=400)

    parameters['norm'] = True if request.args.get('norm') is not None else False

    if (parameters['norm'] and parameters['purple']) or (parameters['norm'] and parameters['white']):
        return Response("ERROR: Cannot have normalization coefficients alongside either purple line points of"
                        " tangency nor/or activated parameter for Illuminant E. PLease, disable one of them. ", status=400)

    return parameters


"""
    Temporary testing endpoint for development. Used to ensure that the finished datapoints give the correct
    data by comparing requests-to-itself with the "absolute truth" (in the shape of .csv files directly and untampered
    from the CIE Functions software).

    Gives a application/json as a result with a boolean value for each endpoint (to indicate if they're correct
    or not correct) - though this will be changed in the future when it is implemented for tests properly. Again,
    this is merely for developmental reasons.
"""
@api.route("/testing", methods=["GET"])
def endpointsTest():
    # creates a dict from function below
    results = endpointsTesting()
    return Response(json.dumps(results), mimetype="application/json", status=200)


def endpointsTesting():
    testingResults = dict()
    # creates a list of tuples in the form of (endpoint, filename of truth)
    endpoints = [('LMS', 'CIE-lms.csv'), ('LMS', 'CIE-LMS-LOG.csv'),
                 ('LMS-MB', 'LMS-MB.csv'), ('LMS-MW', 'CIE-MW.csv')]
    # for each of these in the list ...
    for (endpoint, file) in endpoints:
        # make the request to the url properly; the URL parameters are absolute like this
        # to have the same parameters as the csv files
        url = "http://localhost:5000/" + endpoint + \
              "?mode=result&field_size=2.0&age=32&min=390.0&max=830.0&step-size=1.0"
        if "LOG" in file:
            url += "&log10"
            endpoint = "LMS-log10"
        # get the connection, see if successful
        response = requests.get(url)
        if response.status_code == 200:
            # if it is successful, load the JSON data and create it into a DataFrame
            # as to lessen chances of floating point error occuring
            testing = json.loads(response.content)
            testingDF = pd.DataFrame(testing)
            # the csv file corresponding to the current endpoint is read,
            # float_precision is high to ensure that *all* float decimals are included
            #  (as pandas likes to sometimes round it off at 10 decimals)
            # header=None as there are no headers in the csv file
            original = pd.read_csv(file, float_precision="high", header=None)
            # some CIE functions (like log LMS) confuse the DataFrame by having a column
            # with both floats AND not-a-numerical-numbers that it cannot read as floats
            #  to ensure this won't happen, the original data is treated to numerics
            original = original.apply(pd.to_numeric, errors='coerce')
            # last, the dictionary for current endpoint uses pandas equals to
            # see if original csv DataFrame is equal to the DataFrame from endpoint
            testingResults[endpoint] = (testingDF.equals(original))
        else:
            # if connection fails, it'll show up here
            # (though this won't happen probably)
            testingResults[endpoint] = "Connection failed. "
    return testingResults



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