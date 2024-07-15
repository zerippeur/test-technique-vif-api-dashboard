import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from scipy.signal import resample

try :
    load_dotenv('dashboard/dashboard.env')
except FileNotFoundError:
    pass


API_URI = os.getenv("API_URI")

def get_resampling_method(api_url=f"{API_URI}get_resampling_method") -> str | None:
    """
    Get resampling method.
    Function to get the resampling method from API model.

    Returns
    -------
    str
        Resampling method
    """

    # Set the maximum wait time in seconds
    max_wait_time = 60

    # Loop until the FastAPI app is available or the maximum wait time is reached
    start_time = time.time()
    while True:
        try:
            # Send GET request to API
            response = requests.get(api_url)

            if response.status_code == 200:
                # The FastAPI app is available, so return the result
                result = response.json()
                return result['resampling_method']
            else:
                # The FastAPI app is not available yet, so add a short wait time and retry
                time.sleep(1)
        except requests.exceptions.RequestException as e:
            # A request exception occurred, so add a short wait time and retry
            time.sleep(1)

        # Check if the maximum wait time has been reached
        if time.time() - start_time > max_wait_time:
            # The maximum wait time has been reached, so raise an error
            st.error("Error fetching resampling method from API model")
            return None

def load_data(
        resampling: str='down'
    ) -> tuple[np.ndarray, np.ndarray]:
    """
    Load data
    Function to load the data, resample it according to given strategy and
    eventually shuffle rows to avoid bias.
    Using PS2.txt and FS1.txt as features and profile.txt as target :
    - PS2.txt : 100 Hz
    - FS1.txt : 10 Hz
    - profile.txt : second column
    
    Parameters
    ----------
    resampling : Literal['up', 'down']
        Resampling method
        
    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        data, target
    """
    
    fs1_path = Path("data/FS1.txt")
    fs1_data_up = []
    
    with open(fs1_path) as f:
        x = np.arange(0, 6000, 10)
        for line in f:
            y = np.array([float(x) for x in line.split()])
            fs1_data_up.append(np.interp(np.arange(0, 6000), x, y))
            size_down = len(y)

    with open(fs1_path) as f:
        fs1_data = np.array(
            [float(v) for v in f.read().split()]
        ).reshape(-1, size_down)

    ps2_path = Path("data/PS2.txt")
    
    with open(ps2_path) as f:
        ps2_data = np.array(
            [float(v) for v in f.read().split()]
        ).reshape(-1, 6000)
        ps2_data_down = resample(ps2_data, size_down, axis=-1)

    target = pd.read_csv("data/profile.txt", sep="\t", header=None)[1].values

    if resampling == 'up':
        data = np.stack([np.stack(fs1_data_up), ps2_data], axis=-1)
    elif resampling == 'down':
        data = np.stack([fs1_data, ps2_data_down], axis=-1)

    return (data, target)

def get_valid_cycle_nbs() -> list:
    """
    Get valid cycle nbs.
    Function to get the valid cycle nbs from input data.
    
    Returns
    -------
    list
        Valid cycle nbs
    """
    
    return st.session_state['input'].shape[0]

def get_prediction(
        cycle_input: np.ndarray,
        api_url=f"{API_URI}predict_from_cycle"
    ) -> None:
    """
    Get prediction.
    Function to get the prediction from API model.
    
    Returns
    -------
    str
        Prediction
    """
    json_payload = {'input_data': cycle_input.tolist()}

    # Send POST request to API
    response = requests.post(api_url, json=json_payload)

    if response.status_code == 200:

        result = response.json()
        st.session_state['prediction']['valve_condition'] = result['valve_condition']
        st.session_state['prediction']['confidence'] = result['confidence']

        valve_categories = {
            'optimal': 'Darkturquoise',
            'non-optimal': 'Firebrick'
        }
        result_color = valve_categories[result['valve_condition']]

        st.markdown(
            f"## Valve condition: <span style='color:{result_color}'>{result['valve_condition']}</span>",
            unsafe_allow_html=True
        )
        st.markdown(
            "#### According to our prediction model, the valve has a <span style='color:"
            f"{result_color}'>{result['confidence']*100:.2f}%</span> chance to be in {result['valve_condition']} condition.",
            unsafe_allow_html=True
        )
        return None
    else:
        st.error("Error fetching prediction from API model")
        return None