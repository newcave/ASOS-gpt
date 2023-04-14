import requests
from datetime import datetime, timedelta
import streamlit as st

# set up the API key and endpoint URL
API_URL = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
API_KEY = "egVDA2o6pwjtnUzVIPKzAjyoqYbAfUHumiJ7WrNoWefzLIKzRFnYUSTYQyoacgEcWpNBshNqMQo0n47Q%2FyBsZQ%3D%3D"

# define a function to get weather data for a given date and location
def get_weather_data(date, location):
    # set up the parameters
    params = {
        "serviceKey": API_KEY,
        "dataCd": "ASOS",
        "dateCd": "HR",
        "startDt": date.strftime("%Y%m%d"),
        "startHh": "00",
        "endDt": date.strftime("%Y%m%d"),
        "endHh": "23",
        "stnIds": location,
        "numOfRows": "24",
        "pageNo": "1",
        "_type": "json"
    }

    # make the API request
    response = requests.get(API_URL, params=params)

    # parse the JSON response
    data = response.json()["response"]["body"]["items"]["item"]

    # extract the relevant weather values (temperature, wind speed, humidity)
    temps = [float(d["ta"]) for d in data]
    wind_speeds = [float(d["ws"]) for d in data]
    humidities = [float(d["hm"]) for d in data]

    return temps, wind_speeds, humidities

# define the main function to display the Streamlit app
def main():
    # set up the page title and heading
    st.set_page_config(page_title="ASOS Weather Data", page_icon=":sunny:")
    st.title("ASOS Weather Data")

    # set up the date picker and location selector
    date = st.date_input("Select date", datetime.today() - timedelta(days=1))
    location = st.selectbox("Select location", ["108", "159"])

    # get the weather data
    temps, wind_speeds, humidities = get_weather_data(date, location)

    # display the weather data in a table
    st.write(f"Weather data for {date.date()} in {'Seoul' if location == '108' else 'Busan'}:")
    data = {
        "Time": [f"{i:02d}:00" for i in range(24)],
        "Temperature (°C)": temps,
        "Wind Speed (m/s)": wind_speeds,
        "Humidity (%)": humidities
    }
    st.table(data)

if __name__ == "__main__":
    main()
