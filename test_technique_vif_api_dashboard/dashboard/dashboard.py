import streamlit as st
from dashboard_functions import (get_prediction, get_resampling_method,
                                 get_valid_cycle_nbs, load_data)

# streamlit run dashboard.py
st.set_page_config(layout="wide")
st.title(body='Valve condition prediction app')

tab1, tab2 = st.tabs(
    tabs=[
        ':computer: Valve condition prediction',
        ':clipboard: About'
    ]
)

if 'resampling_method' not in st.session_state:
    st.session_state['resampling_method'] = get_resampling_method()

    if 'data' not in st.session_state:
        st.session_state['data'] = load_data(resampling=st.session_state['resampling_method'])
        st.session_state['input'] = st.session_state['data'][0]
        st.session_state['target'] = st.session_state['data'][1]

if 'cycle_nb' not in st.session_state:
    st.session_state['cycle_nb'] = None

if 'valid_nbs' not in st.session_state:
    st.session_state['valid_nbs'] = {
        'min': 0,
        'max': st.session_state['input'].shape[0] - 1,
    }

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = {
        'valve_condition': None,
        'confidence': None
    }

st.session_state['cycle_nb'] = st.sidebar.number_input(
    label='Cycle number',
    min_value=st.session_state['valid_nbs']['min'],
    max_value=st.session_state['valid_nbs']['max'],
    value=None,
    step=1,
    format='%i',
    placeholder='Enter cycle number'
)

with tab1:
    st.subheader('Valve condition prediction')
    if st.session_state['cycle_nb'] is None:
        st.warning(body='Please enter a cycle number in the sidebar section.', icon="⚠️")
    else:
        with st.container(border=True):
            st.subheader(body='Input data', divider='red')
            st.write(st.session_state['input'][st.session_state['cycle_nb']])
            st.subheader(body='Target data', divider='red')
            st.write(st.session_state['target'][st.session_state['cycle_nb']])
        with st.container(border=True):
            st.subheader(body='Valve condition', divider='red')
            predict = st.button('Predict valve condition', key='predict')
            if predict:
                get_prediction(
                    cycle_input=st.session_state['input'][st.session_state['cycle_nb']],
                )
with tab2:
    st.header(body='Project summary', divider='red')
    st.caption(
        body='This is a technical test for a job opportunity at VIF.   '
             'Please consult README.md for more details.'
    )
    with st.container(border=True):
        st.subheader(body='Related GitHub projects', divider='red')
        st.caption(
            body='This project relies on the following GitHub projects:<br>'
                 'Data loading, model fitting and logging: '
                 '<p><a href='
                 '"https://github.com/zerippeur/test-technique-vif/"'
                 ' target="_blank">test-technique-vif</a></p>'
                 'Prediction API and Dashboard project: '
                 '<p><a href='
                 '"https://github.com/zerippeur/test-technique-vif-api-dashboard/"'
                 ' target="_blank">test-technique-vif-api-dashboard</a></p>',
            unsafe_allow_html=True
        )
    with st.container(border=True):
        st.subheader(body='Dashboard overview', divider='red')
        with st.container():
            st.subheader(body='Sidebar section', divider='grey')
            st.markdown(
                body='Cycle number input'
            )
            st.caption(
                body='Number of the cycle to use as input for the prediction.'
            )
            with st.container():
                st.subheader(body='Tabs', divider='grey')
                col1, col2 = st.columns(2)
                col1.subheader(body='Tab 1: Valve condition prediction')
                col1.caption(
                    body='Shows the cycle input data and sends request to the '
                         'prediction api when clicking on the predict button.'
                )
                col2.subheader(body='Tab 2: About')
                col2.caption(
                    body='Project summary and links to related GitHub projects.'
                )