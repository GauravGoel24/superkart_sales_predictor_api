# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("/content/drive/MyDrive/AI_ML_Course/Model_Deployment/backend_files/superkart_sales_model.pkl")

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sales Predictor API!"

# Define an endpoint for single sales prediction (POST request)
@superkart_sales_predictor_api.post('/v1/predict')
def predict_sale_price():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted sale price as a JSON response.
    """
    # Get the JSON data from the request body
    product_store_data  = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
      'Product_Weight': product_store_data['Product_Weight'],
      'Product_Sugar_Content': product_store_data['Product_Sugar_Content'],
      'Product_Allocated_Area': product_store_data['Product_Allocated_Area'],
      'Product_Type': product_store_data['Product_Type'],
      'Product_MRP': product_store_data['Product_MRP'],
      'Store_Id': product_store_data['Store_Id'],
      'Store_Establishment_Year': product_store_data['Store_Establishment_Year'],
      'Store_Size': product_store_data['Store_Size'],
      'Store_Location_City_Type': product_store_data['Store_Location_City_Type'],
      'Store_Type': product_store_data['Store_Type'],
      'Product_Category_Code': product_store_data['Product_Category_Code'],
      'Store_Age': product_store_data['Store_Age']      
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction 
    predicted_sales = model.predict(input_data)[0]

# Convert prediction to Python float
    predicted_sales = round(float(predicted_sales), 2)
# Convert prediction to Python float
    predicted_sales = round(float(predicted_sales), 2)

# Return the predicted sales revenue
    return jsonify({
        'Predicted Sales Revenue': predicted_sales
    }), 200

# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing property details for multiple sales
    and returns the predicted sales prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all data in the DataFrame
    predicted_sales = model.predict(input_data).tolist()

  # Convert predictions to Python floats and round the values
    predicted_sales = [
        round(float(sales), 2)
        for sales in predicted_sales
    ]

    # Create a dictionary of predictions using record numbers as keys
    output_dict = {
        f'Record_{i+1}': sales
        for i, sales in enumerate(predicted_sales)
    }

    # Return the predictions as a JSON response
    return jsonify(output_dict)

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)
