import math

import requests
from flask import Flask, request, jsonify, make_response, Response, render_template
from flask_cors import CORS

from compute import compute_tabulated, compute_LMS1, my_round, compute_LMS, LMS_energy, chop,\
    Vλ_energy_and_LM_weights, compute_MacLeod_Boynton_diagram, compute_Maxwellian_diagram
import scipy.interpolate
import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time

from computemodularization import compute_MacLeod_Modular, compute_Maxwellian_Modular, compute_LMS_Modular, \
    compute_XYZ_Modular, compute_XY_modular, compute_XYZ_purples_modular, compute_xyz_purples_modular, \
    compute_XYZ_standard_modular, compute_xyz_standard_modular

api = Flask(__name__)
CORS(api)

API_HOMEPAGE = "/API"
API_VERSION = "V1"
LMS_ENDPOINT = "LMS"
LMS_MB_ENDPOINT = "LMS-MB"
LMS_MW_ENDPOINT = "LMS-MW"
XYZ_ENDPOINT = "XYZ"
XY_ENDPOINT = "XY"
XYZP_ENDPOINT = "XYZ-P"
XYP_ENDPOINT = "XY-P"
XYZSTD_ENDPOINT = "XYZ-STD"
XYSTD_ENDPOINT = "XY-STD"
STATUS_ENDPOINT = "STATUS"

server_start = time.time()

def endpoint_creator(homepage, version, endpoint=""):
    all = [homepage, version, endpoint]
    temp = '/'.join(all)
    return temp

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
    # redo so it serves static html instead of this
    return render_template('index.html')

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION))
def APIhome():
    return render_template('api-page.html')


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
        results, plots = compute_LMS1(field_size, age, min, max, step_size)
        """
        field_size, age, min, max, step_size = 2.0, 32, 390.0, 830.0, 1.0
        # N.B! Change the invoced to function to compute_tabulated
        results, plots = compute_LMS1(field_size, age, min, max, step_size)
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
        results, plots = compute_LMS1(field_size, age, min, max, step_size)
        """
        field_size = float(data.get('field_size', 0))
        age = float(data.get('age', 0))
        min = float(data.get('min', 390))
        max = float(data.get('max', 830))
        step_size = float(data.get('step', 1))
        # N.B! Change the invoced to function to compute_tabulated
        results, plots = compute_LMS1(field_size, age, min, max, step_size)
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

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_ENDPOINT), methods=['GET'])
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

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_MB_ENDPOINT), methods=['GET'])
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

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_MW_ENDPOINT), methods=['GET'])
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

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZ_ENDPOINT), methods=['GET'])
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

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, XY_ENDPOINT), methods=['GET'])
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

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZP_ENDPOINT), methods=['GET'])
def xyz_p():
    parameterCheck = createAndCheckParameters(True, compute_XYZ_purples_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        new_calculation_JSON(compute_XYZ_purples_modular,
                          createAndCheckParameters(True, compute_XYZ_purples_modular)),
        mimetype='application/json')

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, XYP_ENDPOINT), methods=['GET'])
def xy_p():
    parameterCheck = createAndCheckParameters(True, compute_xyz_purples_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        new_calculation_JSON(compute_xyz_purples_modular,
                          createAndCheckParameters(True, compute_xyz_purples_modular)),
        mimetype='application/json')

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZSTD_ENDPOINT), methods=['GET'])
def xyz_std():
    parameterCheck = createAndCheckParameters(False, compute_XYZ_standard_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        new_calculation_JSON(compute_XYZ_standard_modular,
                          createAndCheckParameters(False, compute_XYZ_standard_modular)),
        mimetype='application/json')

@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, XYSTD_ENDPOINT), methods=['GET'])
def xy_std():
    parameterCheck = createAndCheckParameters(False, compute_xyz_standard_modular)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if isinstance(parameterCheck, Response):
        return parameterCheck

    return Response(
        new_calculation_JSON(compute_xyz_standard_modular,
                          createAndCheckParameters(False, compute_xyz_standard_modular)),
        mimetype='application/json')



def errorhandler(title, message, suggestion):
    now = datetime.now()
    dict = {
        "status": title,
        "message": message,
        "suggestion": suggestion,
        "timestamp": str(now)
    }
    return json.dumps(dict)

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

    # for all functions except standardization functions:
    if disabled:

        # uses checkArgument to fill in all mandatory parameters
        parameters = {
            # mostly mandatory parameters
            "field_size": request.args.get('field_size', type=float, default=None),
            "age": request.args.get('age', type=float, default=None)
        }

        for (name, value) in parameters.items():
            if value is None:
                return Response(
                    errorhandler("Value Error",
                                 "Invalid input for '{}' due to absence or invalid type.".format(name),
                                 "Please check if '{}' is present, and is of the 'float' type.".format(name)),
                    status=400, mimetype="application/json")
        parameters['age'] = round(parameters['age'])

        # sees if optional parameters present, makes them default to their usual values in the case they are
        # not present
        optionals = {
            "min": request.args.get('min', type=str, default=390.0),
            "max": request.args.get('max', type=str, default=830.0),
            "step_size": request.args.get('step_size', type=str, default=1.0)
        }
        for (name, value) in optionals.items():
            if value is None:
                given = 0
                if name == "min": given = 390.0
                if name == "max": given = 830.0
                if name == "step_size": given = 1.0
                parameters.update({ name: given })
            else:
                try:
                    parameters.update({name: float(value)})
                except ValueError:
                    return Response(
                    errorhandler("Value Error",
                                 "Invalid input for '{}' due to invalid type.".format(name),
                                 "Please check if '{}' is of the 'float' type. Alternatively, "
                                 "you can remove it to use default values.".format(name)),
                    status=400, mimetype="application/json")

        # error handling for the values
        if parameters['field_size'] > 10 or parameters['field_size'] < 1:
            return Response(
                errorhandler("Value Error",
                             "Invalid input for 'field_size'; range is between 1.0-10.0.",
                             "Please check if your 'field_size' is between 1.0 and 10.0."),
                status=422, mimetype="application/json")
        if parameters['age'] < 20 or parameters['age'] > 80:
            return Response(
                errorhandler("Value Error",
                             "Invalid input for 'age': range is between 20-80.",
                             "Please check if your 'age' is between 20-80."),
                status=422, mimetype="application/json")
        if parameters['min'] < 390 or parameters['min'] > 400:
            return Response(
                errorhandler("Value Error",
                             "Invalid input for 'min': range is between 390.0-400.0.",
                             "Please check if your 'min' is between 390.0-400.0."),
                status=422, mimetype="application/json")
        if parameters['max'] > 830 or parameters['max'] < 700:
            return Response(
                errorhandler("Value Error",
                             "Invalid input for 'max': range is between 700.0-830.0.",
                             "Please check if your 'max' is between 700.0-830.0."),
                status=422, mimetype="application/json")
        if parameters['step_size'] > 5 or parameters['step_size'] < 0.1:
            return Response(
                errorhandler("Value Error",
                             "Invalid input for 'step_size': range is between 0.1-5.0.",
                             "Please check if your 'step_size' is between 0.1-5.0."),
                status=422, mimetype="application/json")

        # ----------------------


        # Now, adding optional/specific parameters
        parameters['log'] = True if request.args.get('log10') is not None else False # only for LMS to activate log lms
        parameters['base'] = True if request.args.get('base') is not None else False # only for LMS for base lms

        parameters['info'] = True if request.args.get('info') is not None else False
        parameters['norm'] = True if request.args.get('norm') is not None else False


        # specific 'info' parameter handling:
        if parameters['info'] and (calculation is compute_LMS_Modular or compute_XYZ_standard_modular):
            return Response(
                errorhandler("Value Error",
                             "Invalid usage of 'info' for endpoint. ",
                             "Please verify if this endpoint supports 'info' parameter, and try again. If not, please remove from URL. "),
                status=400, mimetype="application/json")



        # parameter that cannot be triggered by any URL parameter, exclusive to XYZ-purples in usage for compute_xy_modular
        # in order to save time
        parameters['purple'] = False
        # std-xy needs xyz-std, saves time
        parameters['xyz-std'] = False

        return parameters

    else:
        parameters = {"field_size": request.args.get('field_size', type=float, default=None),
                      'info': True if request.args.get('info') is not None else False
                      }

        if parameters['field_size'] == 2.0 or parameters['field_size'] == 10.0:
            return parameters

        return Response(
            errorhandler("Value Error",
                         "Invalid input for 'field_size': Choose between 2.0 or 10.0.",
                         "This endpoint are for standardization functions only, and supports only 2.0 (1931) and 10.0 (1964). Please,"
                         " make sure this is the correct endpoint, and control that your value is one of these two. "),
            status=422, mimetype="application/json")


@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, STATUS_ENDPOINT), methods=["GET"])
def statusEndpoint():
    status = {
        "status": 200,
        "uptime": str(time.time() - server_start) + "s",
        "version": API_VERSION
    }
    return Response(json.dumps(status), mimetype="application/json", status=200)


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