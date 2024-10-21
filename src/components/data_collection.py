from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import wget
import sys
from exception import CustomException
from logger import logging

class DataCollector:
    def __init__(self):
        pass
    
    def initiate_data_collection(self):
        try:
            # Specify the path to ChromeDriver (download and save it on your computer)
            chrome_driver_path = 'chromedriver-win64/chromedriver.exe'

            # Set Chrome options
            chrome_options = Options()
            # Specify the path to the Brave binary
            chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

            # Create a Service object
            service = Service(chrome_driver_path)

            # Create the Chrome driver instance with the options and service
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Open the webpage
            driver.get("https://www.midiworld.com/files/995/")
            logging.info("Web-Driver connected successfully")
            time.sleep(2)


            # Extract all 'li' elements
            elements = driver.find_elements(By.XPATH, "//body/div[1]/div[3]/div[1]/ul/li")
            cnt = 0
            for element in elements:
                if cnt < 250:
                    try:
                        # Extract 'span' elements within each 'li'
                        span_elements = element.find_elements(By.TAG_NAME, 'span')
                        for span in span_elements:
                            name = span.text

                        # Extract 'a' elements within each 'li'
                        a_elements = element.find_elements(By.TAG_NAME, 'a')
                        print(len(a_elements))
                        for a in a_elements:
                            link = a.get_attribute('href')

                        #Download files
                        path = "music_midi"
                        print(name)
                        save_as = os.path.join(path, name + '.mid')
                        wget.download(link, save_as)
                        cnt += 1
                    except:
                        pass
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    data_collector = DataCollector()
    data_collector.initiate_data_collection()
    logging.info('Music files collected successfully.')