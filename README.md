### Create virutual environment and run Flask:
Windows:
.
.
.

Mac OS/Linux:
python3 -m venv venv
source venv/bin/activate
pip install Flask
pip install numpy
pip install scipy

export FLASK_APP=cieapi.py
flask run

### Disable virtual environment:

deactivate