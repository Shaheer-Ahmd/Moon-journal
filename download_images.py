from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
import time
from datetime import date, timedelta

def save_image(url, save_folder, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(save_folder, file_name), 'wb') as f:
            f.write(response.content)

def main():
    # Set up the Chrome WebDriver (ensure you have downloaded and placed it in your PATH)
    driver = webdriver.Chrome()

    try:
        # Define the URL pattern for each day
        base_url = "https://www.webexhibits.org/calendars/moon.html?day={}&month={}&year=2023"
        
        # Define the date range from 21 July 2023 to 21 August 2023
        start_date = date(2023, 7, 21)
        end_date = date(2023, 8, 21)

        # Create a folder to save the images
        save_folder = "moon_images"
        os.makedirs(save_folder, exist_ok=True)

        # Loop through the dates and save the images
        current_date = start_date
        while current_date <= end_date:
            url = base_url.format(current_date.day, current_date.month, current_date.year)
            
            # Open the URL in the browser
            driver.get(url)

            # Wait for some time to let the page load and stabilize
            time.sleep(3)  # Adjust this delay as needed
            
            # Find the image element and extract its source (URL)
            image_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div[2]/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/div/div/div/div[2]/div/div/img')
            image_src = image_element.get_attribute('src')

            # Save the image to the folder
            file_name = f"{current_date.year}_{current_date.month}_{current_date.day}.jpg"
            save_image(image_src, save_folder, file_name)

            # Move to the next date
            current_date += timedelta(days=1)
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
