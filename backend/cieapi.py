import math

import numpy
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
from pathlib import Path
from decimal import Decimal
from array import array
import base64
import sqlite3

from computemodularization import compute_MacLeod_Modular, compute_Maxwellian_Modular, compute_LMS_Modular, \
    compute_XYZ_Modular, compute_XY_modular, compute_XYZ_purples_modular, compute_xyz_purples_modular, \
    compute_XYZ_standard_modular, compute_xyz_standard_modular

api = Flask(__name__)
CORS(api)

calculation_formats = {
    "LMS-base-log":  {
        "result": ["{:.1f}", "{:.8f}", "{:.8f}", "{:.8f}"],
        "plot": ["{:.1f}", "{:.8f}", "{:.8f}", "{:.8f}"],
    },
    "LMS-base": {
        "result": ["{:.1f}", "{:.8e}", "{:.8e}", "{:.8e}"],
        "plot": ["{:.1f}", "{:.8e}", "{:.8e}", "{:.8e}"],
    },
    "LMS-log": {
        "result": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "plot": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
    },
    "LMS": {
        "result": ["{:.1f}", "{:.5e}", "{:.5e}", "{:.5e}"],
        "plot": ["{:.1f}", "{:.5e}", "{:.5e}", "{:.5e}"],
    },
    "Maxwell-Macleod-resplot": {
        "result": ["{:.1f}", "{:.6f}", "{:.6f}", "{:.6f}"],
        "plot": ["{:.1f}", "{:.6f}", "{:.6f}", "{:.6f}"],
    },
    "XYZ-XYZP-XYZ-STD": {
        "result": ["{:.1f}", "{:.6e}", "{:.6e}", "{:.6e}"],
        "plot": ["{:.1f}", "{:.6e}", "{:.6e}", "{:.6e}"],
    },
    "XY-XYP-XY-STD": {
        "result":  ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "plot":  ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
    },
    "info-1": {
        "norm": ["{:.8f}", "{:.8f}", "{:.8f}"],
        "white": ["{:.6f}", "{:.6f}", "{:.6f}"],
        # "white_plot": ["{:.6f}", "{:.6f}", "{:.6f}"],
        "tg_purple": ["{:.6f}", "{:.6f}", "{:.6f}"],
        # "tg_purple_plot": ["{:.6f}", "{:.6f}", "{:.6f}"],
        "xyz_white": ["{:.5f}", "{:.5f}", "{:.5f}"],
        "xyz_tg_purple": ["{:.5f}", "{:.5f}", "{:.5f}"],
        "XYZ_tg_purple": ["{:.5f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "trans_mat": ["{:.8f}", "{:.8f}", "{:.8f}"],
        # "trans_mat_N": ["{:.8f}", "{:.8f}", "{:.8f}"],
    }
}

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
    endpoints_description = Path('api-page.txt').read_text()
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


def JSON_writer(results, formatting):
    """
    A function which takes in a results ndarray as well as an expected format to output the JSON string.
    Parameters
    ----------
    results
    format

    Returns
    -------

    """

    result = []
    if type(results) == dict:
        temp = []
        # if the dictionary is result/plot, not info
        if (list(results.keys())) == ["result", "plot"]:
            for name, body in results.items():
                start = '"{}":'.format(name)
                if len(body) == 1:
                    body = [body]
                if "white" in name:
                    start += JSON_writer(body, formatting)
                else:
                    start += JSON_writer(chop(body), formatting)
                temp.append(start)
            output = ','.join(temp)
        return "{" + output + "}"
    else:
        for row in results:
            (w, l, m, s) = row
            if math.isinf(s):
                s = "null"
                format = formatting[:28] + "{s}]"
                result.append(format.format(w=w, l=l, m=m, s=s))
            else:
                result.append(formatting.format(w=w, l=l, m=m, s=s))

        output = ','.join(result)
        return "[" + output + "]"

def calculation_to_JSON(calculation, parameters):
    """
    calculation_to_JSON is a function that outputs a JSON string based on the result array given and the parameters.
    While the previous iteration of the API used pandas dataframes to avoid the problem of floating point errors,
    this was not feasible for results of high precision due to many significant figures.

    This function is the new iteration for the API; it saves the numbers as formatted strings exactly like the
    original software does - ensuring the exact same numbers as the software.
    Parameters
    ----------
    calculation: The function responsible for the calculations.
    parameters: A dictionary containing the URL parameters.

    Returns
    -------
    A string which acts as a JSON output for an API.
    """

    if parameters['info']:
        return "placeholder"

    if calculation is compute_LMS_Modular:
        if parameters['base']:
            if parameters['log']:
                # log10 base LMS
                return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.8f}, {m:.8f}, {s:.8f}]")
            else:
                # base LMS
                return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.8e}, {m:.8e}, {s:.8e}]")
        else:
                # log10 LMS
            if parameters['log']:
                return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.5f}, {m:.5f}, {s:.5f}]")
            else:
                # LMS
                return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.5e}, {m:.5e}, {s:.5e}]")

    # many of these share the same ones
    if calculation in [compute_Maxwellian_Modular, compute_MacLeod_Modular]:
        return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.6f}, {m:.6f}, {s:.6f}]")
    if calculation in [compute_XYZ_Modular, compute_XYZ_purples_modular, compute_XYZ_standard_modular]:
        return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.6e}, {m:.6e}, {s:.6e}]")
    else:
        return JSON_writer(calculation(parameters), "[{w:.1f}, {l:.5f}, {m:.5f}, {s:.5f}]")


def new_calculation_JSON(calculation, parameters):

    if parameters['info']:
        return write_to_JSON(calculation(parameters), calculation_formats['info-1'])

    if calculation is compute_LMS_Modular:
        if parameters['base']:
            if parameters['log']:
                # log10 base LMS
                return write_to_JSON(calculation(parameters), calculation_formats['LMS-base-log'])
            else:
                # base LMS
                return write_to_JSON(calculation(parameters), calculation_formats['LMS-base'])
        else:
                # log10 LMS
            if parameters['log']:
                return write_to_JSON(calculation(parameters), calculation_formats['LMS-log'])
            else:
                # LMS
                return write_to_JSON(calculation(parameters), calculation_formats['LMS'])
    # many of these share the same ones
    if calculation in [compute_Maxwellian_Modular, compute_MacLeod_Modular]:
        return write_to_JSON(calculation(parameters), calculation_formats["Maxwell-Macleod-resplot"])
    if calculation in [compute_XYZ_Modular, compute_XYZ_purples_modular, compute_XYZ_standard_modular]:
        return write_to_JSON(calculation(parameters), calculation_formats["XYZ-XYZP-XYZ-STD"])
    else:
        return write_to_JSON(calculation(parameters), calculation_formats["XY-XYP-XY-STD"])

def write_to_JSON(results_dict, json_dict):
    """
    Step b, should first get a dictionary of all elements with their JSONified ndarrays,
    before it then makes *that* dictionary into a JSON string itself.

    Parameters
    ----------
    results_dict
    json_dict

    Returns
    -------

    """
    something = {}
    for (name, body) in results_dict.items():
        something[name] = ndarray_to_JSON(body, json_dict[name])
    output = []
    for (name, body) in something.items():
        temp = '"{}":'.format(name) + body
        output.append(temp)
    fin = ','.join(output)
    return '{' + fin + '}'

def ndarray_to_JSON(body, formatta):
    """
    Should in theory deliver an ndarray formatted to JSON, no matter dimensions - only exception is that
    the array contents, whatever they are, are the same structure as formatta. So, for example,
    [[[3, 2, 1]]] needs a formatta of [some, thing, here]. The function won't work on ndarrays that are therefore
    not structured right and consistent.
    Parameters
    ----------
    body
    formatta

    Returns
    -------

    """
    # for later consideration; have it return a value that is not dict nor array
    # if (not isinstance(body, dict)) and (not isinstance(body, numpy.ndarray)):
    if body.ndim == 1:
        if len(body) == len(formatta):
            all = []
            for index in range(len(body)):
                # for -inf in log10 LMS
                tempar = chop(body[index])
                asda = formatta[index]
                if math.isinf(body[index]):
                    tempar = "null"
                    asda = "{}"
                all.append(asda.format(tempar))
            output = ','.join(all)
            return '[' + output + ']'
        else:
            return "Something is wrong here ..."
    else:
        temp = []
        for row in body:
            temp.append(ndarray_to_JSON(row, formatta))
        output = ','.join(temp)
        return '[' + output + ']'

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
        new_calculation_JSON(compute_LMS_Modular,
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
        new_calculation_JSON(compute_MacLeod_Modular,
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
            new_calculation_JSON(compute_Maxwellian_Modular,
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
            new_calculation_JSON(compute_XYZ_Modular,
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
        new_calculation_JSON(compute_XY_modular,
                          createAndCheckParameters(True, compute_XY_modular)),
        mimetype='application/json')

@api.route('/XYZ-P', methods=['GET'])
def xyz_p():
    parameterCheck = createAndCheckParameters(True, compute_XYZ_purples_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        calculation_to_JSON(compute_XYZ_purples_modular,
                          createAndCheckParameters(True, compute_XYZ_purples_modular)),
        mimetype='application/json')

@api.route('/XY-P', methods=['GET'])
def xy_p():
    parameterCheck = createAndCheckParameters(True, compute_xyz_purples_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        calculation_to_JSON(compute_xyz_purples_modular,
                          createAndCheckParameters(True, compute_xyz_purples_modular)),
        mimetype='application/json')

@api.route('/XYZ-STD', methods=['GET'])
def xyz_std():
    parameterCheck = createAndCheckParameters(False, compute_XYZ_standard_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        calculation_to_JSON(compute_XYZ_standard_modular,
                          createAndCheckParameters(False, compute_XYZ_standard_modular)),
        mimetype='application/json')

@api.route('/XY-STD', methods=['GET'])
def xy_std():
    parameterCheck = createAndCheckParameters(False, compute_xyz_standard_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        calculation_to_JSON(compute_xyz_standard_modular,
                          createAndCheckParameters(False, compute_xyz_standard_modular)),
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

    if disabled:
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

        # Now, adding optional/specific parameters
        parameters['log'] = True if request.args.get('log10') is not None else False # only for LMS to activate log lms
        parameters['base'] = True if request.args.get('base') is not None else False # only for LMS for base lms

        parameters['info'] = True if request.args.get('info') is not None else False
        parameters['norm'] = True if request.args.get('norm') is not None else False
        # parameter that cannot be triggered by any URL parameter, exclusive to XYZ-purples in usage for compute_xy_modular
        # in order to save time
        parameters['xyz-purple'] = False
        # std-xy needs xyz-std, saves time
        parameters['xyz-std'] = False

        return parameters
    else:
        parameters = {
            "mode": checkArgument('mode', str),
            "field_size": checkArgument('field_size', int)
        }

        if parameters['mode'] not in ['plot', 'result']:
            return Response("ERROR: Parameter 'mode' is not properly set. Please use either 'plot' or 'result'.", status=400)

        parameters['white'] = True if request.args.get('white') is not None else False # for XY-std
        parameters['purple'] = True if request.args.get('purple') is not None else False # for XY-std
        if parameters['purple'] and parameters['white']:
            return Response("ERROR: Cannot have parameters 'white' and 'purple' activated at the same time. Please, "
                            "disable one of them. ", status=400)

        if parameters['field_size'] == 2 or parameters['field_size'] == 10:
            return parameters

        return Response("ERROR: The standard functions only support field sizes of 2° (1931) and 10° (1964). "
                "Please change your field-size.", status=400)


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
        ('XY', '/XY?mode=result&field_size=2.3&age=25&min=391.7&max=829.1&step-size=0.6', 'CIE-XY.csv'),
        ('XY-PLOT', '/XY?mode=plot&field_size=1.5&age=35&min=390.0&max=829.2&step-size=0.1', 'CIE-XY-PLOT.csv'), # needs less precision, 0.xxxxx
        ('XY-P', '/XY-P?mode=result&field_size=3.4&age=45&min=390.0&max=829.8&step-size=0.6', 'CIE-XY-P.csv'),
        ('XYZ-STD', '/XYZ-STD?mode=result&field_size=2', 'CIE-XYZ-STD.csv'), # needs less precision
        ('XY-STD', '/XY-STD?mode=plot&field_size=10', 'CIE-XY-STD.csv'),
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

            if not testingResults[name]:
                print("wait.")
            print(testingResults[name], name)
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