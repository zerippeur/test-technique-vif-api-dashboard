import os

import mlflow
import numpy as np
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

# 2. Create app and model objects
app = FastAPI()

try:
    load_dotenv('api/api.env')
except FileNotFoundError:
    pass

MLFLOW_TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]
MLFLOW_TRACKING_USERNAME = os.environ["MLFLOW_TRACKING_USERNAME"]
MLFLOW_TRACKING_PASSWORD = os.environ["MLFLOW_TRACKING_PASSWORD"]
MLFLOW_MODEL_URI = os.environ["MLFLOW_MODEL_URI"]

mlflow.set_tracking_uri(uri=MLFLOW_TRACKING_URI)

model = mlflow.keras.load_model(model_uri=MLFLOW_MODEL_URI)

def get_resampling_method_from_model_path(model_path):
    # Split the string into a list of substrings
    substrings = model_path.split('__')

    # Iterate over the substrings and check if it contains "Resampling"
    for substring in substrings:
        if 'Resampling' in substring:
            # Extract the resampling method using split() again
            resampling_method = substring.split('_')[-1]
            break

    return resampling_method

@app.get('/get_resampling_method')
def get_resampling_method()-> dict:
    """
    Function to get resampling method.

    Returns:
        resampling_method: A dictionary with the resampling method.
    """
    resampling_method = get_resampling_method_from_model_path(str(MLFLOW_MODEL_URI))
    method_dict = {
        'resampling_method': resampling_method
    }

    return method_dict

@app.post('/predict_from_cycle')
async def predict_valve_condition(json_payload: dict)-> dict:
    """
    Function to predict valve condition from cycle input.

    Parameters:
        cycle_dict: dictionary containing cycle input.

    Returns:
        prediction_dict: A dictionary with the valve condition prediction.
    """

    input_data = np.reshape(np.array(json_payload['input_data']), (1, 6000, 2))

    prediction = model.predict(input_data)

    valve_condition = 'optimal' if np.argmax(prediction) == 3 else 'non-optimal'
    if valve_condition == 'optimal':
        confidence = float(np.max(prediction))
    else:
        confidence = float(1 - prediction[0,3])

    prediction_dict = {
        'valve_condition': valve_condition,
        'confidence': confidence
    }

    return prediction_dict


# 4. Run the API with uvicorn (uvicorn api.app:app --reload)
# first app stands for the pyhton file, second app for the API instance,
#--reload for automatic refresh
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)