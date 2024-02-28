# Frontend setup
1. navigate to frontend/cie-react
2. npm install
4. npm install recharts
5. npm install react-router-dom
5. npm install react-plotly.js plotly.js
5. npm run dev 

Accessible at http://localhost:5173/

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

Accessible at http://localhost:5000/

### Mac OS/Linux:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install Flask
3. pip install flask-cors
4. pip install numpy
5. pip install scipy
6. export FLASK_APP=cieapi.py
7. flask run

Accessible at http://localhost:5000/

### Disable virtual environment:

deactivate