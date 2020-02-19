# Install libraries

pip install -r requirements.txt

# Running the app

python app.py

# Running the tests

pytest .

# Running test with coverage

pytest . -v  --cov-report html --cov=app test/ 
