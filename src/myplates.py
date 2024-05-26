from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
import os.path

#make this the location of the words database
DATA_LOCATION = os.path.join('..', '.config', 'Urban Words.csv')
#make this the location of your chrome driver
CHROME_DRIVER_LOCATION = os.path.join('..', '..', 'chrome-win64', 'chrome-win64', 'chrome.exe')


df = pd.read_csv(DATA_LOCATION)

# Path to the Chrome browser executable
chrome_path = CHROME_DRIVER_LOCATION
# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path
# Initialize Chrome WebDriver with options
driver = webdriver.Chrome(options=chrome_options)
# Open the website
driver.get('https://www.myplates.com.au/create-plate')
# Wait for the page to load
driver.implicitly_wait(10)  # Adjust as necessary

def CLICK(xpath):
    # Wait for the third accordion to become clickable
    accordion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    # Click on the third accordion to open it
    accordion.click()
    # Wait for the content to load
    time.sleep(1)  # Adjust based on the site's response time

def type_in_field(xpath, text):
    # Find the input field by XPath
    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    # Clear the existing text in the field (if any)
    input_field.clear()
    # Type the desired text into the field
    input_field.send_keys(text)

def clear_text(xpath):
    # Clear the existing text in the field
    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    input_field.clear()

CLICK("/html/body/app-root/app-home/app-body/div[2]/div/div/div/div/div[1]/div/app-new-combination/div/div[2]/div/div[2]/div/div[1]/div[1]")


def find_next_word_to_do():
    i = 0
    availability_list = df["Availability"]
    print(availability_list[:20])
    for i in range(len(availability_list)):
        if availability_list[i] == False or availability_list[i] == True:
            i+=1
        else:
            return i

starting_position = find_next_word_to_do()

while starting_position < len(df['Word']):
    word = df['Word'][starting_position]
    clean_word = re.sub('[^0-9a-zA-Z]+', '', word)
    type_in_field("/html/body/app-root/app-home/app-body/div[2]/div/div/div/div/div[1]/div/app-new-combination/div/div[3]/div/div[2]/input", clean_word)
    CLICK("/html/body/app-root/app-home/app-body/div[2]/div/div/div/div/div[1]/div/app-new-combination/div/div[3]/div/div[3]/app-button/button")
    clear_text("/html/body/app-root/app-home/app-body/div[2]/div/div/div/div/div[1]/div/app-new-combination/div/div[3]/div/div[2]/input")
    output = driver.find_element(By.XPATH, "/html/body/app-root/app-home/app-body/div[2]/div/div/div/div/div[1]/div/app-new-combination/div")
    df['Availability'][starting_position] = "This combination is available" in output.text
    df.to_csv(DATA_LOCATION, index=False)
    starting_position += 1

# Close the browser
driver.quit()
