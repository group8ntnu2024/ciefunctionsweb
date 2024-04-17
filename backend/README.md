# Backend, short notes

## v2

### General Information

Ver. 2.0 uses the `Sanic`, replacing `Flask` as the server framework due to the fast nature and asynchronicity for
handling requests. Also replaces `unittest` with `pytest` as module for testing due to support of asynchronous handles
for testing endpoints.

### How to Use

To run the server, use this command in the terminal:
```
    sanic cieapi.api --workers=4
```

To run tests and see coverage, use the following commands in terminal:
```
    coverage run -m pytest cieapi_test.py
    coverage report -i -m
```

## v1

placeholder ..

## 

Mac

 pip install Sanic 
 pip install setuptools 
 pip install requests    
 pip install flask-cors
 pip install numpy
 pip install scipy
 pip install pandas