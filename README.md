# Frontend setup
1. navigate to frontend/cie-react
2. npm install
3. npm run dev


# Backend setup
### Windows:
1. Navigate to backend directory
2. Enter command "python -m venv venv" to create virtual environment
3. Enter command ".\venv\Scripts\activate"
4. Enter command "pip install Flask"
5. Enter command "pip install flask-cors"
6. Enter command "pip install numpy"
7. Enter command "pip install scipy"
8. Enter command "python cieapi.py"

### Mac OS/Linux:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install Flask
3. pip install flask-cors
4. pip install numpy
5. pip install scipy
6. export FLASK_APP=cieapi.py
7. flask run

### Disable virtual environment:

deactivate