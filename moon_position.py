from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import pandas as pd

def implement_pre_zero_regex(s: str) -> str:
    if s[0] != '0' and int(s) < 10:
        return "0" + s
    return s

def deg_to_float(deg: str) -> float:
    return float(deg[:-1])

def get_azimuth_altitude_coordinates(time_separation: float):
    driver = webdriver.Chrome()
    try:
        start_date = datetime(2023, 7, 20)
        end_date = datetime(2023, 8, 17)
        current_time = datetime(2023, 7, 20, 20, 0, 0) # for minutes and hours 

        i = 0
        current_date = start_date
        # time_separation = 50.5
        azimuth = []
        altitude = []
        moon_phase_name_list = []
        moon_phase_percentage_list = []
        while current_date <= end_date:
            cdy = str(current_date.year)
            cdm = implement_pre_zero_regex(str(current_date.month))
            cdd = implement_pre_zero_regex(str(current_date.day))

            driver.get(f'https://www.mooncalc.org/#/35.2979,75.6337,15/{cdy}.{cdm}.{cdd}/{current_time.hour}:{current_time.minute}/1/3')
            
            # Extract Azimuth and Altitude coordinates using XPaths
            azimuth_element = driver.find_element(By.XPATH, '/html/body/div[7]/div[4]/table/tbody/tr[6]/td[2]/span')
            altitude_element = driver.find_element(By.XPATH, '/html/body/div[7]/div[4]/table/tbody/tr[5]/td[2]/span')
            moon_phase_info = driver.find_element(By.XPATH, '/html/body/div[7]/div[4]/table/tbody/tr[9]/td[1]/acronym[1]/span')
            #moon_phase_info = Phase Name/Phase Percentage (Full Moon/97%)
            moon_phase_name = moon_phase_info.text.split('/')[0]
            moon_phase_percentage = moon_phase_info.text.split('/')[1].split('%')[0]

            # Append the extracted values to the respective lists
            azimuth.append(deg_to_float(azimuth_element.text))
            altitude.append(deg_to_float(altitude_element.text))
            moon_phase_name_list.append(moon_phase_name)
            moon_phase_percentage_list.append(moon_phase_percentage)

            current_time += timedelta(minutes=time_separation)
            current_date += timedelta(days=1)
            i += 1

    finally:
        driver.quit()

    # Return the extracted Azimuth and Altitude coordinates as lists
    return azimuth, altitude, moon_phase_name_list, moon_phase_percentage_list

if __name__ == "__main__":
    azimuth_list, altitude_list, mpnl, mpnp = get_azimuth_altitude_coordinates(time_separation=25)

    # Create a DataFrame from the azimuth and altitude lists
    data = {
        'Azimuth': azimuth_list,
        'Altitude': altitude_list,
        'Phase name': mpnl,
        'Phase percentage': mpnp
    }
    df = pd.DataFrame(data)

    # Save the DataFrame to a new Excel file with numbering in name
    print(df)

    df.to_excel('moon_coordinates_help.xlsx', index=False)