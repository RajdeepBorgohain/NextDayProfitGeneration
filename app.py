import streamlit as st
import pandas as pd
import datetime
import numpy as np
import datetime
import all_model

def show_information():
    # Show Information about the selected Stock
    st.header('🤫Did you know💡')
    st.caption("Analyzing data from 2015 to 2021")
    st.text("1) There is a 60% chance of gap up opening in any random trade in Reliance 😮 ")
    st.text("2) 1% of the gap up is more than Rs:15.00 i.e more quantity == more profit😇")
    st.text("3) Median, Q3 or 75th percentile have increased from 2015(1.8) to 2021(11.55)💰")

def select_date():
    # Select the date for Prediction
    selected_date = st.date_input(
        "Which date you want to check",
        datetime.date(2022, 3, 6))
    st.write('Your selected date is:', selected_date)
    
    return selected_date

# @st.cache
# def prepare_data_for_selected_date():
#     df = pd.read_csv("dataset/reliance_30min.csv")
#     df = helper.format_date(df)
#     df = helper.replace_vol(df)
#     df = helper.feature_main(df)
#     df.to_csv('dataset/processed_reliance30m.csv')
    
#     return df

@st.cache
def freature_data(date):
    # st.dataframe(df.loc[str(date)])
    df = pd.read_csv("dataset/processed_reliance30m.csv",parse_dates=['Datetime']).set_index('Datetime')
    df = df.loc[str(date)]
    df = df.drop(columns=['date'],axis=1)
    
    
    return df


def show_prediction_result(prepared_data):
    model = all_model.load_model()
    result = all_model.prediction(model,prepared_data)
    
    return result
    


def main():
    st.title('PROFIT IN THE MORNING!')
    option = st.selectbox(
        'Which stock would you like to analyze?',
        ('None','Reliance', 'Airtel', 'State Bank Of India'))

    st.write('You selected:', option)



    if option=="Reliance":
        data_link = ("C:/Users/Rajdeep Borgohain.000/Desktop/reliance_30min.csv")
        dateSelect = False
        # About Reliance Stock
        show_information()
        selected_date = select_date()
        # prepared_data = prepare_data_for_selected_date()
        prepared_data = freature_data(selected_date)
        score = show_prediction_result(prepared_data)
        st.write('')
        selected_date+=datetime.timedelta(days=1)
        
        if score == 'nan':
            text = f'No data avaliable for the selected date {selected_date}'
            st.warning(text)
        elif score >= 0.5:
            score = np.round(score,4)*100
            text = f'The chances of Gap up on:      {selected_date}     is      {score}%'
            st.success(text)
        elif score < 0.5:
            text = f'The chances of Gap up on: {selected_date}  is  {score}'
            st.error(text)
    else:
        st.text('Data Not Avaliable!')
        
if __name__ == "__main__":
    main()