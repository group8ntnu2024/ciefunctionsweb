import math

import requests
# from flask import Flask, request, jsonify, make_response, Response, render_template
from flask_cors import CORS

from compute import compute_tabulated, compute_LMS1, my_round, compute_LMS, LMS_energy, chop, \
    Vλ_energy_and_LM_weights, compute_MacLeod_Boynton_diagram, compute_Maxwellian_diagram
import scipy.interpolate
import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time
# from gevent.pywsgi import WSGIServer
from sanic import Sanic, response
from sanic.response import json, html

from computemodularization import compute_MacLeod_Modular, compute_Maxwellian_Modular, compute_LMS_Modular, \
    compute_XYZ_Modular, compute_XY_modular, compute_XYZ_purples_modular, compute_xyz_purples_modular, \
    compute_XYZ_standard_modular, compute_xyz_standard_modular

api = Sanic(__name__)

API_HOMEPAGE = "/api"
API_VERSION = "v2"
LMS_ENDPOINT = "lms"
LMS_MB_ENDPOINT = "lms-mb"
LMS_MW_ENDPOINT = "lms-mw"
XYZ_ENDPOINT = "xyz"
XY_ENDPOINT = "xy"
XYZP_ENDPOINT = "xyz-p"
XYP_ENDPOINT = "xy-p"
XYZSTD_ENDPOINT = "xyz-std"
XYSTD_ENDPOINT = "xy-std"
STATUS_ENDPOINT = "status"

server_start = time.time()


def endpoint_creator(homepage, version, endpoint=""):
    all = [homepage, version, endpoint]
    temp = '/'.join(all)
    return temp


calculation_formats = {
    "LMS-base-log": {
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
        "result": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "plot": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
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


@api.get('/')
async def home(request):
    # redo so it serves static html instead of this
    content = Path('./templates/index.html').read_text()
    return html(content)


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION))
async def APIhome(request):
    content = Path('./templates/api-page.html').read_text()
    return html(content)


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


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_ENDPOINT))
async def LMS(request):
    parameterCheck = createAndCheckParameters(True, compute_LMS_Modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(new_calculation_JSON(compute_LMS_Modular,
                                             createAndCheckParameters(True, compute_LMS_Modular, request)),
                        content_type="application/json")


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_MB_ENDPOINT))
async def MB(request):
    parameterCheck = createAndCheckParameters(True, compute_MacLeod_Modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(new_calculation_JSON(compute_MacLeod_Modular,
                                             createAndCheckParameters(True, compute_MacLeod_Modular, request)),
                        content_type="application/json")


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_MW_ENDPOINT))
async def maxwellian(request):
    parameterCheck = createAndCheckParameters(True, compute_Maxwellian_Modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(new_calculation_JSON(compute_Maxwellian_Modular,
                                             createAndCheckParameters(True, compute_Maxwellian_Modular, request)),
                        content_type="application/json")


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZ_ENDPOINT))
async def xyz(request):
    parameterCheck = createAndCheckParameters(True, compute_XYZ_Modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(new_calculation_JSON(compute_XYZ_Modular,
                                             createAndCheckParameters(True, compute_XYZ_Modular, request)),
                        content_type="application/json")


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XY_ENDPOINT))
async def xy(request):
    parameterCheck = createAndCheckParameters(True, compute_XY_modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(
        new_calculation_JSON(compute_XY_modular,
                             createAndCheckParameters(True, compute_XY_modular, request)),
        content_type="application/json"
    )


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZP_ENDPOINT))
async def xyz_p(request):
    parameterCheck = createAndCheckParameters(True, compute_XYZ_purples_modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(
        new_calculation_JSON(compute_XYZ_purples_modular,
                             createAndCheckParameters(True, compute_XYZ_purples_modular, request)),
        content_type="application/json"
    )


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYP_ENDPOINT))
async def xy_p(request):
    parameterCheck = createAndCheckParameters(True, compute_xyz_purples_modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(
        new_calculation_JSON(compute_xyz_purples_modular,
                             createAndCheckParameters(True, compute_xyz_purples_modular, request)),
        content_type="application/json"
    )


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZSTD_ENDPOINT))
async def xyz_std(request):
    parameterCheck = createAndCheckParameters(False, compute_XYZ_standard_modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(
        new_calculation_JSON(compute_XYZ_standard_modular,
                             createAndCheckParameters(False, compute_XYZ_standard_modular, request)),
        content_type="application/json"
    )


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYSTD_ENDPOINT))
async def xy_std(request):
    parameterCheck = createAndCheckParameters(False, compute_xyz_standard_modular, request)
    # parameterCheck may either be a dictionary (which means that all parameters are alright),
    # or a Response object (which means that a mandatory parameter is not filled, so calculations
    # cannot proceed further).
    if "error" in parameterCheck.keys():
        return response.json(parameterCheck, status=parameterCheck["status_code"])

    return response.raw(
        new_calculation_JSON(compute_XYZ_standard_modular,
                             createAndCheckParameters(False, compute_XYZ_standard_modular, request)),
        content_type="application/json"
    )


@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, STATUS_ENDPOINT), methods=["GET"])
def statusEndpoint(request):
    status = {
        "status": 200,
        "uptime": str(time.time() - server_start) + "s",
        "version": API_VERSION
    }
    return response.json(status, status=200)


def errorhandler(title, status, message, suggestion):
    now = datetime.now()
    dict = {
        "error": title,
        "status_code": status,
        "message": message,
        "suggestion": suggestion,
        "timestamp": str(now)
    }
    return dict


def createAndCheckParameters(disabled, calculation, request):
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

    # error handling
    def string_to_type_else(string, type, other):
        # try to make the string into an instance of type
        try:
            return type(string)
        # if it cannot be converted to type, then return the "other"
        except ValueError:
            return other
        # however, if there is a typerror (such as passing None to float()), then return None
        except TypeError:
            return None

    # for all functions except standardization functions:
    if disabled:
        # uses checkArgument to fill in all mandatory parameters
        parameters = {
            # mostly mandatory parameters
            "field_size": string_to_type_else(request.args.get('field_size'), float, None),
            "age": string_to_type_else(request.args.get('age'), float, None)
        }

        # checks if mandatory parameters are present
        for (name, value) in parameters.items():
            if value is None:
                return errorhandler("Value Error",
                                    422,
                                    "Invalid input for '{}' due to absence or invalid type.".format(name),
                                    "Please check if '{}' is present, and is of the 'float' type.".format(name))
        parameters['age'] = round(parameters['age'])

        # sees if optional parameters present, makes them default to their usual values in the case they are
        # not present
        optionals = {
            # are either None (if arg is not present at all),
            # a float value if the arg is present and is a float,
            # or a -1 if the arg is present, but not float
            "min": string_to_type_else(request.args.get('min'), float, -1),
            "max": string_to_type_else(request.args.get('max'), float, -1),
            "step_size": string_to_type_else(request.args.get('step_size'), float, -1),
        }

        for (name, value) in optionals.items():
            # if not correct type
            if value is -1:
                return errorhandler("Value Error",
                                    422,
                                    "Invalid input for '{}' due to invalid type.".format(name),
                                    "Please check if '{}' is of the 'float' type. Alternatively, "
                                    "you can remove it to use default values.".format(name))
            # if not present at all
            if value is None:
                given = 0
                if name == "min": given = 390.0
                if name == "max": given = 830.0
                if name == "step_size": given = 1.0
                parameters.update({name: given})
            # if present and correct type
            else:
                parameters.update({name: float(value)})

        # error handling for the values
        if parameters['field_size'] > 10 or parameters['field_size'] < 1:
            return errorhandler("Value Error",
                                422,
                                "Invalid input for 'field_size'; range is between 1.0-10.0.",
                                "Please check if your 'field_size' is between 1.0 and 10.0.")
        if parameters['age'] < 20 or parameters['age'] > 80:
            return errorhandler("Value Error",
                                422,
                                "Invalid input for 'age': range is between 20-80.",
                                "Please check if your 'age' is between 20-80.")
        if parameters['min'] < 390 or parameters['min'] > 400:
            return errorhandler("Value Error",
                                422,
                                "Invalid input for 'min': range is between 390.0-400.0.",
                                "Please check if your 'min' is between 390.0-400.0.")
        if parameters['max'] > 830 or parameters['max'] < 700:
            return errorhandler("Value Error",
                                422,
                                "Invalid input for 'max': range is between 700.0-830.0.",
                                "Please check if your 'max' is between 700.0-830.0.")
        if parameters['step_size'] > 5 or parameters['step_size'] < 0.1:
            return errorhandler("Value Error",
                                422,
                                "Invalid input for 'step_size': range is between 0.1-5.0.",
                                "Please check if your 'step_size' is between 0.1-5.0.")

        # ----------------------

        optionals = {
            'log': False,
            'base': False,
            'info': False,
            'norm': False
        }

        # if there is anything with "optional" in URL
        if request.args.get('optional') is not None:
            # split it by the comma to make a list of entries
            params = request.args.get('optional').split(',')
            # for every element in this list, see if it exists in the optional parameter dictionary keys; if it does,
            # then make that key's body True
            for param in params:
                if param in optionals.keys():
                    optionals[param] = True
                else:
                    return errorhandler("Value Error",
                                        422,
                                        "Optional parameter list contains unknown optional parameter.",
                                        "Please control that the list contains only valid parameters, and try again.")
            # else, if it is not in it, then throw error

        for (name, body) in optionals.items():
            if body:
                if (name == "log" or name == "base") and (calculation is not compute_LMS_Modular):
                    return errorhandler("Value Error",
                                        422,
                                        "Invalid usage of {} for endpoint.".format(name),
                                        "The {} is exclusive to the /LMS endpoint. Please, remove it from your URL.".format(name))
                if (name == "info") and (calculation is compute_LMS_Modular):
                    return errorhandler("Value Error",
                                        422,
                                           "Invalid usage of 'info' for endpoint. ",
                                         "Please verify if this endpoint supports 'info' parameter, and try again. If not, please remove from URL. ")
                if (name == "norm") and (calculation in [compute_LMS_Modular, compute_MacLeod_Modular, compute_Maxwellian_Modular]):
                    return errorhandler("Value Error",
                                        422,
                                        "Invalid usage of 'norm' for endpoint. ",
                                        "Please verify if this endpoint supports 'norm' parameter, and try again. If not, please remove from URL. ")

            parameters.update({
                name: body
            })

        # parameter that cannot be triggered by any URL parameter, exclusive to XYZ-purples in usage for compute_xy_modular
        # in order to save time
        parameters['purple'] = False
        # std-xy needs xyz-std, saves time
        parameters['xyz-std'] = False

        return parameters

    else:
        parameters = {"field_size": string_to_type_else(request.args.get('field_size'), float, None)}
        if parameters['field_size'] is None:
            return errorhandler("Value Error", 422, "Invalid value type for field_size parameter.",
                                "Please check if your field_size is a float value that is either 2.0 or 10.0.")

        optionals = {
            'log': False,
            'base': False,
            'info': False,
            'norm': False
        }

        # if there is anything with "optional" in URL
        if request.args.get('optional') is not None:
            # split it by the comma to make a list of entries
            params = request.args.get('optional').split(',')
            # for every element in this list, see if it exists in the optional parameter dictionary keys; if it does,
            # then make that key's body True
            for param in params:
                if param in optionals.keys():
                    optionals[param] = True
                else:
                    return errorhandler("Value Error",
                                        422,
                                        "Optional parameter list contains unknown optional parameter.",
                                        "Please control that the list contains only valid parameters, and try again.")
            # else, if it is not in it, then throw error

        for (name, body) in optionals.items():
            if body == None:
                if body is None:
                    parameters.update({name: False})
                    continue
            if body:
                if (name == "log" or name == "base"):
                    return errorhandler("Value Error",
                                        422,
                                        "Invalid usage of {} for endpoint.".format(name),
                                        "The {} is exclusive to the /LMS endpoint. Please, remove it from your URL.".format(name))
                if (name == "info") and (calculation is compute_XYZ_standard_modular):
                    return errorhandler("Value Error",
                                        422,
                                        "Invalid usage of 'info' for endpoint. ",
                                        "Please verify if this endpoint supports 'info' parameter, and try again. If not, please remove from URL. ")
                if (name == "norm"):
                    return errorhandler("Value Error",
                                        422,
                                        "Invalid usage of parameter norm for endpoint. ",
                                        "Please verify if this endpoint supports 'norm' parameter, and try again. If not, please remove from URL. ")
            parameters.update({
                name: body
            })

        if parameters['field_size'] == 2.0 or parameters['field_size'] == 10.0:
            return parameters

        return errorhandler("Value Error",
                            422,
                            "Invalid input for 'field_size': Choose between 2.0 or 10.0.",
                            "This endpoint are for standardization functions only, and supports only 2.0 (1931) and 10.0 (1964). Please,"
                            " make sure this is the correct endpoint, and control that your value is one of these two. ")


if __name__ == '__main__':
    api.run(debug=True, port=8080)

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
