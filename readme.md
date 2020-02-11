#install libraries
pip install -r requirements.txt

#running the up
python app.py

#running test
pytest .

#running tests with coverage
pytest . -v --cov-report html --cov=app tests/
