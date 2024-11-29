import os
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,  # Set the minimum logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("scraping.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)




# Function to extract and save institute data
def extract_and_save_institute_data(container_element, filename=None):
    """
    Extracts data from the given 'rightContainer1' div element and saves it as a JSON file.
    :param container_element: Selenium WebElement representing the 'rightContainer1' div.
    :param filename: Optional custom filename for the JSON file. If not provided, the institute code will be used.
    """
    # Locate the 'Institute Summary' fields within the container
    institute_code = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblInstituteCode').text
    institute_name = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblInstituteName').text
    institute_address = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblInstituteAddress').text
    region = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblRegion').text
    district = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblDistrict').text
    status = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblStatus1').text
    autonomy_status = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblStatus2').text
    minority_status = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblStatus3').text
    public_remark = container_element.find_element(By.ID, 'rightContainer_ContentBox1_lblPublicRemark').text

    # Locate the 'Course Details' table and extract data row by row
    course_details = []
    rows = container_element.find_elements(By.XPATH, ".//table[@id='rightContainer_ContentBox7_gvChoiceCodeList']//tr")[1:]  # Skip header row

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        course = {
            "choice_code": columns[0].text,
            "course_name": columns[1].text,
            "university": columns[2].text,
            "status": columns[3].text,
            "autonomy_status": columns[4].text,
            "minority_status": columns[5].text,
            "shift": columns[6].text,
            "accreditation": columns[7].text,
            "gender": columns[8].text,
            "total_intake": columns[9].text
        }
        course_details.append(course)

    # Create a dictionary structure for the JSON data
    data = {
        "institute_summary": {
            "institute_code": institute_code,
            "institute_name": institute_name,
            "institute_address": institute_address,
            "region": region,
            "district": district,
            "status": status,
            "autonomy_status": autonomy_status,
            "minority_status": minority_status,
            "public_remark": public_remark
        },
        "course_details": course_details
    }

    # If filename is not provided, use institute code as filename
    if not filename:
        filename = f"2023-24/institute_{institute_code}.json"

    # Save the data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data has been saved to {filename}")


# Function to scrape all colleges from the list
def scrape_colleges():
    # Set up the Chrome driver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the website
    url = 'https://fe2023.mahacet.org/StaticPages/frmInstituteList?did=1884'
    driver.get(url)

    # Create a folder to store the JSON files if it doesn't exist
    if not os.path.exists("2023-24"):
        os.makedirs("2023-24")

    # Find the table element with all college rows
    table = driver.find_element(By.ID, "rightContainer_ContentTable1_gvInstituteList")
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for i in range(1, len(rows) + 1):  # Start from 1 to avoid header row
        try:
            # Click on the anchor tag in each row (except the header)
            link = driver.find_element(By.XPATH, f"""//*[@id="rightContainer_ContentTable1_gvInstituteList"]/tbody/tr[{i+1}]/td[2]/a"""  )
            print("Link Selected !")
            link.click()
            print("Link Clicked !")

            # Wait for the new page to load (you might want to use WebDriverWait for better synchronization)
            time.sleep(2)

            # Find the container element with class 'rightContainer1'
            container_element = driver.find_element(By.ID, 'rightContainer1')
            print("Found container!")

            # Extract and save the data using the previously defined function
            extract_and_save_institute_data(container_element)
            print("Saved Data")

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        finally:

            # Go back to the previous page
            driver.get(url)

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    scrape_colleges()
