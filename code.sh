# Create a virtual environment (recommended)
python -m venv venvkprsnt
source venv\Scripts\activate  # On Windows use `venv\Scripts\activate`

# Install necessary libraries
pip install dash dash-bootstrap-components pandas plotly

# Create requirements.txt
pip freeze > requirements.txt