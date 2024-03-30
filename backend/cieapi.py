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

from computemodularization import compute_MacLeod_Modular, compute_Maxwellian_Modular, compute_LMS_Modular, \
    compute_XYZ_Modular, compute_XY_modular

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
        The optional parameters above can be used together and combined.
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

-   CIE cone-fundamental-based XYZ tristimulus functions
    Path: /XYZ
    Method: GET
    Parameters:
        'mode': Either 'plot' or 'result' for the type of return
        'field_size': A float number for the field size wished
        'age': An integer detailing the age wished for computation
        'min': Minimum value of domain
        'max': Maximum value of domain
        'step_size': The size of steps for each computation
        'norm': Optional with no value needed, gives renormalized values
        'trans': Optional with no value needed, gives the transformation matrix of linear transformation LMS --> XYZ.
        The optional parameters above can be used together and combined.
        
-   CIE cone-fundamental-based xyz chromaticity coordinates
    Path: /XY
    Method: GET
    Parameters:
        'mode': Either 'plot' or 'result' for the type of return
        'field_size': A float number for the field size wished
        'age': An integer detailing the age wished for computation
        'min': Minimum value of domain
        'max': Maximum value of domain
        'step_size': The size of steps for each computation
        'white': Optional with no value needed; gives values for Illuminant E. Cannot be used with 'purple' activated.
        'purple': Optional with no value needed; gives values for purple line's point of tangency with spectrum locus. Cannot be used when 'white' is activated.
        'norm': Optional with no value needed, gives renormalized values. Can be used with all other optional parameters.
        'XYZ': Optional with no value needed, provides values with precision of 7 sign. figs. Otherwise, provides
        precision of 5 sign. figs. Can only be used when parameter 'purple' is activated.

-   Testing Endpoint
    Path: /testing
    Method: GET
    Parameters:
        NONE
    Note: 
        This is a developmental testing endpoint, used temporarily in development alongside debugging tools to ensure:
        1. That each endpoint calculates the right values given parameters.
        2. That each endpoint dispenses/outputs these values correctly and exactly as intended.
        The rests return a Boolean, indicating if they succeded (true) or not (false) - and they cover the usual
        expected tests of values for plot and result, in addition to testing if the program is resistant to false-
        positives in regards to test.


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
    Beware: "double_precision" cannot be too high nor too low. Too high will cause wavelengths to have
    floating point precision problems (example, 390.99999999999999 == 391) - but too low will cause
    the other values to start experiencing it. If it happens again, experiment with this value first.

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
    pd.set_option("display.precision", 11)
    pd.set_option("styler.format.precision", 11)
    if parameters['mode'] == "plot" and ((calculation is compute_Maxwellian_Modular) or
    (calculation is compute_MacLeod_Modular)):
        # precision of floats in plots for macleod and maxwellian have to be tuned down to fit
        # similar numbers from the .csv
        return pd.DataFrame(calculation(parameters)).to_json(orient="values", double_precision=6)
    if calculation is compute_MacLeod_Modular:
        return pd.DataFrame(calculation(parameters)).to_json(orient="values", double_precision=6)
    return pd.DataFrame(calculation(parameters)).to_json(orient="values", double_precision=13)

"""
    The endpoints for the API. 
    
    All of these functions are near identical, with the only exception being what calculation
    function they pass onto wrapperDictionary. Other than that, they're all endpoint functions for each
    respective endpoint.
"""

@api.route('/LMS', methods=['GET'])
def LMS():
    parameterCheck = createAndCheckParameters(True, compute_LMS_Modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        wrapperDictionary(compute_LMS_Modular,
                          createAndCheckParameters(True, compute_LMS_Modular)),
        mimetype='application/json')

@api.route('/LMS-MB', methods=['GET'])
def MB():
    parameterCheck = createAndCheckParameters(True, compute_MacLeod_Modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        wrapperDictionary(compute_MacLeod_Modular,
                          createAndCheckParameters(True, compute_MacLeod_Modular)),
        mimetype='application/json')

@api.route('/LMS-MW', methods=['GET'])
def maxwellian():
        parameterCheck = createAndCheckParameters(True, compute_Maxwellian_Modular)
        # parameterCheck may either be a dictionary (which means that all parameters are alright),
        # or a Response object (which means that a mandatory parameter is not filled, so calculations
        # cannot proceed further).
        if isinstance(parameterCheck, Response):
            return parameterCheck

        return Response(
            wrapperDictionary(compute_Maxwellian_Modular,
                              createAndCheckParameters(True, compute_Maxwellian_Modular)),
                                mimetype='application/json')

@api.route('/XYZ', methods=['GET'])
def xyz():
        parameterCheck = createAndCheckParameters(True, compute_XYZ_Modular)
        # parameterCheck may either be a dictionary (which means that all parameters are alright),
        # or a Response object (which means that a mandatory parameter is not filled, so calculations
        # cannot proceed further).
        if isinstance(parameterCheck, Response):
            return parameterCheck

        return Response(
            wrapperDictionary(compute_XYZ_Modular,
                              createAndCheckParameters(True, compute_XYZ_Modular)),
                                mimetype='application/json')

@api.route('/XY', methods=['GET'])
def xy():
    parameterCheck = createAndCheckParameters(True, compute_XY_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        wrapperDictionary(compute_XY_modular,
                          createAndCheckParameters(True, compute_XY_modular)),
        mimetype='application/json')


def createAndCheckParameters(disabled, calculation):

    """

    Parameters
    ----------
    disabled: A boolean which will enable/disable the checking of most parameters except for field_size
    (which is necessary for CIE XYZ std colour-matching funcs and CIE xy std cromaticity diagram).
    calculation: The calculation function that the parameters are to be used on; mostly included for
    the sake of optional parameter management.

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
    if parameters['λ_min'] < 390 or parameters['λ_min'] > 400:
        return Response("ERROR: Minimum domain must be between 390 and 400 nm. "
                        "Please change the min domain input.", status=400)
    if parameters['λ_max'] > 830 or parameters['λ_max'] < 700:
        return Response("ERROR: Maximum domain must be between 700 and 830 nm. "
                        "Please change the max domain input. ", status=400)
    if parameters['λ_step'] > 5 or parameters['λ_step'] < 0.1:
        return Response("ERROR: Invalid step size. Please input a value of nm between 0.1 and 5.0.", status=400)

    # adjusting parameter maximum domain in accordance to step-size
    if (parameters['λ_max'] - parameters['λ_min']) % parameters['λ_step'] is not 0:
        parameters['λ_max'] = parameters['λ_min'] + ((parameters['λ_max'] - parameters['λ_min']) -
                                                     ((parameters['λ_max'] - parameters['λ_min']))
                                                     % parameters['λ_step'])

    # Now, adding optional/specific parameters
    parameters['log'] = True if request.args.get('log10') is not None else False # only for LMS to activate log lms
    parameters['base'] = True if request.args.get('base') is not None else False # only for LMS for base lms
    parameters['white'] = True if request.args.get('white') is not None else False # for MacLeod, Maxwellian, XY
    parameters['purple'] = True if request.args.get('purple') is not None else False # for MacLeod, Maxwellian, XY
    parameters['norm'] = True if request.args.get('norm') is not None else False # for MacLeod, Maxwellian, XYZ, XY
    parameters['trans'] = True if request.args.get('trans') is not None else False # for XYZ
    parameters['XYZ'] = True if request.args.get('XYZ') is not None else False  # for XY-diagram

    # really specific endpoint optional parameter checking now
    if parameters['purple'] and parameters['white']:
        return Response("ERROR: Cannot have parameters 'white' and 'purple' activated at the same time. Please, "
                        "disable one of them. ", status=400)
    if calculation is not compute_LMS_Modular:
        if parameters['log']: return Response("ERROR: Log10 parameter is exclusive to /LMS endpoint, and is not supported"
                                              " on your current endpoint; please disable it. ", status=400)
        if parameters['base']: return Response("ERROR: Base parameter is exclusive to /LMS endpoint, and is not supported "
                                               "on your current endpoint; please disable it.", status=400)
    if calculation is not compute_XYZ_Modular:
        if parameters['trans']: return Response("ERROR: Parameter 'trans' for transformational matrix of linear transformation "
                                                "LMS -> XYZ is exclusive to the /XYZ endpoint; please disable it. ", status=400)

    if (calculation is not compute_Maxwellian_Modular) and (calculation is not compute_MacLeod_Modular)\
            and (calculation is not compute_XY_modular) and (calculation is not compute_XYZ_Modular) :
        if (parameters['purple'] or parameters['white'] or parameters['norm']):
            return Response("ERROR: Parameters 'purple', 'white' and 'norm' cannot be used with your current endpoint. "
                            "Please, remove them from the URL and try again. ", status=400)

    if calculation is not compute_XY_modular:
        if parameters['XYZ']: return Response("ERROR: Parameter 'XYZ' is exclusive to the /XY endpoint. Please, disable it.",
                                              status=400)
    else:
        if parameters['XYZ'] and not parameters['purple']: return Response("ERROR: Parameter 'XYZ' can only be used when parameter 'purple'"
                                                                           "is activated. Please, enable it. ", status=400)
    if calculation is compute_MacLeod_Modular or calculation is compute_Maxwellian_Modular:
        if (parameters['norm'] and parameters['purple']) or (parameters['norm'] and parameters['white']):
            return Response("ERROR: Parameter 'norm' does not work alongside parameters 'white' nor 'purple' for the"
                            " Macleod-Boyton and Maxwellian CIE functions. Please, disable one. ", status=400)

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
    # creates a list of tuples in the form of (key, endpoint url, file)
    endpoints = [
        ('LMS', '/LMS?mode=result&field_size=2.0&age=20&min=390.0&max=830.0&step-size=1.0', 'CIE-LMS.csv'),
        ('LMS-LOG10', '/LMS?mode=result&field_size=2.5&age=52&min=390.0&max=828.0&step-size=1.5&log10', 'CIE-LMS-LOG.csv'),
        ('LMS-BASE', '/LMS?mode=result&field_size=1.5&age=70&min=400.0&max=700.0&step-size=1.0&base', 'CIE-LMS-BASE.csv'),
        ('LMS-PLOT', '/LMS?mode=plot&field_size=1.0&age=30&min=400.0&max=700.0&step-size=1.0', 'CIE-LMS-PLOT.csv'),
        ('MB', '/LMS-MB?mode=result&field_size=2.0&age=69&min=390.0&max=810.0&step-size=1.2', 'CIE-LMS-MB.csv'),
        ('MB-PLOT', '/LMS-MB?mode=plot&field_size=1.0&age=45&min=400.0&max=700.0&step-size=1.2', 'CIE-LMS-MB-PLOT.csv'),
        ('MW', '/LMS-MW?mode=result&field_size=1.5&age=71&min=399.0&max=702.5&step-size=0.5', 'CIE-LMS-MW.csv'),
        ('MW-PLOT', '/LMS-MW?mode=plot&field_size=2.9&age=80&min=400.0&max=700.0&step-size=0.5', 'CIE-LMS-MW-PLOT.csv'),
        ('XYZ', '/XYZ?mode=result&field_size=2.0&age=36&min=390.0&max=830.0&step-size=0.8', 'CIE-XYZ.csv'),
        ('XYZ-NORM', '/XYZ?mode=result&field_size=2.5&age=20&min=390.0&max=829.6&step-size=1.4&norm', 'CIE-XYZ-NORM.csv'),
        ('XYZ-PLOT', '/XYZ?mode=plot&field_size=4.0&age=38&min=400.0&max=700.0&step-size=0.1&norm', 'CIE-XYZ-PLOT.csv'),
        ('false-pos-1', '/LMS?mode=result&field_size=2.0&age=19&min=390.0&max=830.0&step-size=1.0', 'CIE-LMS.csv'),
        ('false-pos-2', '/LMS-MB?mode=result&field_size=2.0&age=23&min=390.0&max=810.0&step-size=1.2', 'CIE-LMS-MB.csv'),
        ('false-pos-3', '/LMS-MW?mode=plot&field_size=2.0&age=11&min=400.0&max=700.0&step-size=0.5', 'CIE-LMS-MW-PLOT.csv')
    ]
    # for each of these in the list ...
    for (name, endpoint, file) in endpoints:
        # get the connection, see if successful
        url = "http://localhost:5000" + endpoint
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
            filepath = "./data/tests/" + file
            original = pd.read_csv(filepath, float_precision="high", header=None)
            # some CIE functions (like log LMS) confuse the DataFrame by having a column
            # with both floats AND not-a-numerical-numbers that it cannot read as floats
            #  to ensure this won't happen, the original data is treated to numerics
            original = original.apply(pd.to_numeric, errors='coerce')
            # last, the dictionary for current endpoint uses pandas equals to
            # see if original csv DataFrame is equal to the DataFrame from endpoint
            # debugging tester, shows differences between dataframes to easier
            # see the cause of unequalness
            # tester = testingDF.compare(original)
            testingResults[name] = (testingDF.equals(original))
            # the false-pos tests will return a false initially to indicate that the
            # API dataframe and the csv dataframe are not identical, this just reverses it
            # so that it shows that it passed the test
            if "false" in name:
                testingResults[name] = not testingResults[name]
            # print(testingResults[name], name)
        else:
            # if connection fails, it'll show up here
            # (though this won't happen probably)
            testingResults[name] = "-"
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