import json
import pytest

import numpy as np
import pandas as pd

import cieapi as cieapi

# the API will have to serialize its own JSONs directly by making a custom JSON string,
# so a lint test is required to see if the JSONs produced are valid and true
def json_lint_test(json_string):
    try:
        json.loads(json_string)
    except ValueError:
        return False
    return True

# simple test case for ndarray_to_JSON
def test_ndarray_to_JSON():
    format = ['{:.3f}', '{:.3f}', '{:.3f}', '{:.3f}']
    basic = np.array([1.0, 2.0, 3.0, 4.0])
    assert "[1.000,2.000,3.000,4.000]" == cieapi.ndarray_to_JSON(basic, format)
    assert json_lint_test(cieapi.ndarray_to_JSON(basic, format)) == True

# advanced and realistic case
def test_advanced_ndarray_to_JSON():
    advanced = np.array([[0.8934598, 0.87234879, 123.3453, 1239.234],
                         [0.3982475, 0.8438345, 253.00, 2545.4385],
                         [0.234854, 0.348589, 7554.45, 9523.4755]])
    format = ['{:.7f}', '{:.7f}', '{:.5e}', '{:.5e}']
    answer = ("[[0.8934598,0.8723488,1.23345e+02,1.23923e+03],"
              "[0.3982475,0.8438345,2.53000e+02,2.54544e+03],"
              "[0.2348540,0.3485890,7.55445e+03,9.52348e+03]]")
    assert answer == cieapi.ndarray_to_JSON(advanced, format)
    assert json_lint_test(cieapi.ndarray_to_JSON(advanced, format)) == True

# testing writing a dict with ndarrays to JSON
def test_write_to_JSON():
    format = {
        "example": ["{:.3f}", "{:.3f}", "{:.3f}", "{:.3f}"],
    }
    case = {
        "example": np.array([
            [234.1248, 1232.3874, 0.00245, 0.43533],
            [754.1234, 0.35475, 0.00245, 0.43533],
            [9595.243, 4573.324, 1.1111, 45345.232]
        ])
    }
    answer = ('{"example":[[234.125,1232.387,0.002,0.435],'
              '[754.123,0.355,0.002,0.435],'
              '[9595.243,4573.324,1.111,45345.232]]}')
    assert answer == cieapi.write_to_JSON(case, format)
    assert json_lint_test(cieapi.write_to_JSON(case, format)) == True


# testing the endpoint creator function to see if it creates correct URLs
def test_endpoint_creator():
    assert "/home/v10/testingendpoint" == cieapi.endpoint_creator(
        "/home", "v10", "testingendpoint")


# tests the home page, see if it returns html and 200
@pytest.mark.asyncio
async def test_home_endpoint():
    req, response = await cieapi.api.asgi_client.get("/")
    assert response.status == 200

@pytest.mark.asyncio
async def test_wrong_endpoint():
    req, response = await cieapi.api.asgi_client.get("/asdasdasd")
    assert response.status == 404

@pytest.mark.asyncio
async def test_api_endpoint():
    req, response = await cieapi.api.asgi_client.get("/api/v2/")
    assert response.status == 200


def load_csv_to_array(file_path):
    return pd.read_csv(file_path, header=None).to_numpy()

# tests lms endpoint
@pytest.mark.asyncio
async def test_lms_endpoint():
    truth_data = load_csv_to_array("./tests/LMS-1-25-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms?field_size=1&age=25")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# tests macleod endpoint
@pytest.mark.asyncio
async def test_lmsmb_endpoint():
    truth_data = load_csv_to_array("./tests/LMS-MB-5-63-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms-mb?field_size=5&age=63")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# tests maxwellian endpoint
@pytest.mark.asyncio
async def test_lmsmw_endpoint():
    truth_data = load_csv_to_array("./tests/LMS-MW-45-45-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms-mw?field_size=4.5&age=45")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# tests XYZ endpoint
@pytest.mark.asyncio
async def test_xyz_endpoint():
    truth_data = load_csv_to_array("./tests/XYZ-38-52-15.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xyz?field_size=3.8&age=52&step_size=1.5")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# tests XY endpoint

@pytest.mark.asyncio
async def test_xy_endpoint():
    truth_data = load_csv_to_array("./tests/XY-31-71-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy?field_size=3.1&age=71")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# tests xy-purple endpoint,
# cannot test xyz-purples due to crashing software, cannot retrieve csv
@pytest.mark.asyncio
async def test_xyp_endpoint():
    truth_data = load_csv_to_array("./tests/XYP-20-32-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-p?field_size=2&age=32")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# testing standardization function for xyz
@pytest.mark.asyncio
async def test_xyzstd_endpoint():
    truth_data = load_csv_to_array("./tests/XYZ-STD-2.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xyz-std?field_size=2")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200

# testing standardization function for xy
@pytest.mark.asyncio
async def test_xystd_endpoint():
    truth_data = load_csv_to_array("./tests/XY-STD-2.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-std?field_size=2")
    assert np.all(np.array(json.loads(response.body)['plot']) == truth_data) == True
    assert response.status == 200

# testing various parameters

@pytest.mark.asyncio
async def test_param1_endpoint():
    test_case = ('{"norm":[0.6993641,0.34253216,0.03040997],"white":[0.71312,0.28688,0.016007],"tg_purple":[[409.5,'
            '0.663468,0.951054],[699.9,0.969648,0]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms-mb?field_size=1.5&age=51&max=700&optional=info")
    assert json.loads(response.body) == json.loads(test_case)

@pytest.mark.asyncio
async def test_param2_endpoint():
    test_case = ('{"white":[0.333300,0.333330,0.333370],"tg_purple":[[360.200000,0.182210,0.019980],'
                   '[700.900000,0.720360,0.279640]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-std?field_size=10.0&optional=info")
    assert json.loads(response.body) == json.loads(test_case)

@pytest.mark.asyncio
async def test_param3_endpoint():
    test_case = ('{"xyz_white":[0.33333,0.33333,0.33333],"xyz_tg_purple":[[409.70000,0.16304,0.01656],[703.30000,'
                  '0.72329,0.27671]],"XYZ_tg_purple":[[409.70000,0.08657,0.00879,0.43561],[703.30000,0.00863,0.00330,'
                  '0.00000]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-p?field_size=2&age=32&optional=info")
    assert json.loads(response.body) == json.loads(test_case)

@pytest.mark.asyncio
async def test_param4_endpoint():
    test_case = ('{"trans_mat":[[1.93122240,-1.42718225,0.40529507],[0.68367008,0.35153487,0.00000000],[0.00000000,'
                  '0.00000000,1.94811216]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/xyz-p?field_size=2.0&age=20&optional=info")
    assert json.loads(response.body) == json.loads(test_case)



