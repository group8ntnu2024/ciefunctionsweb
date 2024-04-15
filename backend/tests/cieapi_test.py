import json
import math
import unittest

import numpy as np
import pandas as pd

import cieapi as cieapi


class CIEAPITesting(unittest.TestCase):
    # the API will have to serialize its own JSONs directly by making a custom JSON string,
    # so a lint test is required to see if the JSONs produced are valid and true
    def json_lint_test(self, json_string):
        try:
            json.loads(json_string)
        except ValueError:
            return False
        return True

    # simple test case for ndarray_to_JSON
    def test_ndarray_to_JSON(self):
        format = ['{:.3f}', '{:.3f}', '{:.3f}', '{:.3f}']
        basic = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertEqual("[1.000,2.000,3.000,4.000]", cieapi.ndarray_to_JSON(basic, format))
        self.assertEqual(self.json_lint_test(cieapi.ndarray_to_JSON(basic, format)), True)

    # advanced and realistic case
    def test_advanced_ndarray_to_JSON(self):
        advanced = np.array([[0.8934598, 0.87234879, 123.3453, 1239.234],
                             [0.3982475, 0.8438345, 253.00, 2545.4385],
                             [0.234854, 0.348589, 7554.45, 9523.4755]])
        format = ['{:.7f}', '{:.7f}', '{:.5e}', '{:.5e}']
        answer = ("[[0.8934598,0.8723488,1.23345e+02,1.23923e+03],"
                  "[0.3982475,0.8438345,2.53000e+02,2.54544e+03],"
                  "[0.2348540,0.3485890,7.55445e+03,9.52348e+03]]")
        self.assertEqual(answer, cieapi.ndarray_to_JSON(advanced, format))
        self.assertEqual(self.json_lint_test(cieapi.ndarray_to_JSON(advanced, format)), True)

    # testing writing a dict with ndarrays to JSON
    def test_write_to_JSON(self):
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
        self.assertEqual(answer, cieapi.write_to_JSON(case, format))
        self.assertEqual(self.json_lint_test(cieapi.write_to_JSON(case, format)), True)

    # testing the endpoint creator function to see if it creates correct URLs
    def test_endpoint_creator(self):
        self.assertEqual("/home/v10/testingendpoint", cieapi.endpoint_creator(
            "/home", "v10", "testingendpoint"))

    # function that sets up a testing API client
    def api_test_client_setup(self):
        cieapi.api.config['TESTING'] = True
        self.client = cieapi.api.test_client()

    # tests the home page, see if it returns html and 200
    def test_home_endpoint(self):
        self.api_test_client_setup()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    # tests the status page, sees if it gives correct status and version
    def test_status_endpoint(self):
        self.api_test_client_setup()
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], 200)
        self.assertEqual(response.json["version"], "v1")

    # testing faulty data in endpoint
    def test_faulty_data_endpoint(self):
        self.api_test_client_setup()
        response = self.client.get("/api/v1/lms?age=243")
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 400)

    # testing not found endpoint
    def test_notfound_endpoint(self):
        self.api_test_client_setup()
        # wrong endpoint because it should be lowercase lms, not LMS
        response = self.client.get("/api/v1/LMS?field_size=2&age=24")
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 404)


    def compare_endpoints(self, csv_file, endpoint_url, type):
        """
        Compares the result between endpoint (from url) and actual truth answer (from csv made directly from software).
        Parameters
        ----------
        csv_file    : File path to .csv
        endpoint_url: URL to endpoint
        type    : String, either "plot" or "result" for the ndarray one wishes from endpoint result dict

        Returns
        -------
        Boolean that is:
            True if the endpoint and csv file are the same (meaning the endpoint outputs same data as csv file)
            False if the endpoint has different numbers than the csv file (meaning wrong numbers)

        """
        response = self.client.get(endpoint_url)
        self.assertEqual(response.status_code, 200)
        csv = np.genfromtxt(csv_file, delimiter=',', dtype=float)
        return np.array_equal(csv, np.array(response.json[type]))

    # tests the LMS endpoint
    def test_lms_endpoint(self):
        self.api_test_client_setup()
        self.assertEqual(True, self.compare_endpoints("./tests/LMS-1-25-1.CSV", "/api/v1/lms?field_size=1&age=25", "result"))
        self.assertEqual(True, self.compare_endpoints("./tests/LMS-1-25-01.CSV", "/api/v1/lms?field_size=1&age=25", "plot"))

        # testing base and log

        # the csv contains ' -inf', which is treated as a string - the dataframe makes the entire column
        # therefore string, even the floats; goes through the column and makes it either None (corresponding to
        # null in JSON when retrieved into Python) or the float of the string
        def changer(data):
            empty = []
            for cell in data:
                if cell == ' -inf':
                    empty.append(None)
                else:
                    empty.append(float(cell))
            return empty

        response = self.client.get("api/v1/lms?field_size=2&age=20&log10&base").json
        res_test = pd.read_csv("./tests/LMS-2-20-1-log-base.CSV", header=None)
        res_test_array = res_test.to_numpy()
        # reformats ' -inf' column to either number or None
        res_test_array[:, 3] = changer(res_test_array[:, 3])
        self.assertEqual((np.array(response['result']) == res_test_array).all(), True)

    # tests MacLeod endpoint
    def test_macleod_endpoint(self):
        self.api_test_client_setup()
        self.assertEqual(True, self.compare_endpoints("./tests/LMS-MB-5-63-1.csv", "/api/v1/lms-mb?field_size=5&age=63", "result"))
        self.assertEqual(True, self.compare_endpoints("./tests/LMS-MB-5-63-01.csv", "/api/v1/lms-mb?field_size=5&age=63", "plot"))

    # tests Maxwellian endpoint
    def test_maxwell_endpoint(self):
        self.api_test_client_setup()
        self.assertEqual(True, self.compare_endpoints("./tests/LMS-MW-45-45-1.csv", "/api/v1/lms-mw?field_size=4.5&age=45", "result"))
        self.assertEqual(True, self.compare_endpoints("./tests/LMS-MW-45-45-01.csv", "/api/v1/lms-mw?field_size=4.5&age=45", "plot"))

    # tests XYZ endpoint
    def test_XYZ_endpoint(self):
        self.api_test_client_setup()
        self.assertEqual(True, self.compare_endpoints("./tests/XYZ-38-52-15.csv", "/api/v1/xyz?field_size=3.8&age=52&step_size=1.5", "result"))
        self.assertEqual(True, self.compare_endpoints("./tests/XYZ-38-52-01.csv", "/api/v1/xyz?field_size=3.8&age=52&step_size=1.5", "plot"))

    # tests XY endpoint
    def test_XY_endpoint(self):
        self.api_test_client_setup()
        self.assertEqual(True, self.compare_endpoints("./tests/XY-31-71-1.csv", "/api/v1/xy?field_size=3.1&age=71", "result"))
        self.assertEqual(True, self.compare_endpoints("./tests/XY-31-71-01.csv", "/api/v1/xy?field_size=3.1&age=71", "plot"))

    # tests the standardization function endpoints
    def test_std_endpoints(self):
        self.api_test_client_setup()
        self.assertEqual(True, self.compare_endpoints("./tests/XYZ-STD-2.csv", "/api/v1/xyz-std?field_size=2", "result"))
        self.assertEqual(True, self.compare_endpoints("./tests/XY-STD-2.csv", "/api/v1/xy-std?field_size=2", "plot"))

    # tests different endpoints with alternative parameters
    def test_special_parameter_endpoints(self):
        self.api_test_client_setup()
        # intentionally faulty url (trying to get info from LMS endpoint)
        response = self.client.get("api/v1/lms?field_size=2.0&age=23&log10&max=700&min=400&info")
        self.assertNotEqual(response.status_code, 200)

        def test_json(json_string, url):
            answer = json.loads(json_string)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(answer, response.json)

        test_json('{"norm":[0.6993641,0.34253216,0.03040997],"white":[0.71312,0.28688,0.016007],"tg_purple":[[409.5,'
                  '0.663468,0.951054],[699.9,0.969648,0]]}', "/api/v1/lms-mb?field_size=1.5&age=51&max=700&info")
        test_json('{"white":[0.333300,0.333330,0.333370],"tg_purple":[[360.200000,0.182210,0.019980],[700.900000,'
                  '0.720360,0.279640]]}', "/api/v1/xy-std?field_size=10.0&info")
        test_json('{"xyz_white":[0.33333,0.33333,0.33333],"xyz_tg_purple":[[409.70000,0.16304,0.01656],[703.30000,'
                  '0.72329,0.27671]],"XYZ_tg_purple":[[409.70000,0.08657,0.00879,0.43561],[703.30000,0.00863,0.00330,'
                  '0.00000]]}', "/api/v1/xy-p?field_size=2&age=32&info")
        test_json('{"trans_mat":[[1.93122240,-1.42718225,0.40529507],[0.68367008,0.35153487,0.00000000],[0.00000000,'
                  '0.00000000,1.94811216]]}', "/api/v1/xyz-p?field_size=2.0&age=20&info")


if __name__ == '__main__':
    unittest.main()
