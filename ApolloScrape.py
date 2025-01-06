import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

# Set up Chrome options
options = Options()
options.add_argument('user-data-dir=C://Users//jjkam//AppData//Local//Google//Chrome//User Data//Profile 1')

driver = webdriver.Chrome(options=options)

driver.get("https://app.apollo.io/#/login?redirectTo=https%3A%2F%2Fapp.apollo.io%2F%23%2Fonboarding-hub%2Fqueue")
time.sleep(5)

# Read the company names from the CSV file
company_df = pd.read_csv(r'C:\Users\jjkam\Downloads\Copy of Attending_Companies_2024 - Attending_Companies_2024 (11).csv')  # Update with the path to your CSV file
companies = company_df.iloc[:, 0].tolist()  # Assumes the first column contains the company names

data = pd.DataFrame(columns=['Company', 'Name', 'Position', 'Email'])

def get_css_selector(element):
    path = []
    while element.tag_name != 'html':
        sibling_count = 0
        sibling_index = 0
        for sibling in element.find_elements(By.XPATH, 'preceding-sibling::*'):
            if sibling.tag_name == element.tag_name:
                sibling_count += 1
        path.append(f"{element.tag_name}:nth-of-type({sibling_count + 1})")
        element = element.find_element(By.XPATH, '..')
    path.reverse()
    return ' > '.join(path)

def ScrapeInfo(company):
    try:
        Email = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#main-app > div.zp_GhGgo > div > div > div.zp_HrbxN > div:nth-child(1) > div.page-header.zp_yfwnw > div.zp_I8qdp > div.zp_cu0dr > div.zp_MGlfT.zp_IsAWH > div.zp_FvUYj.zp_u83Uf > div > div.zp_gOECT > div > div:nth-child(1) > div > div > div > div.zp_w0Cv0.zp_EXndU > div.zp_TNVkG.zp_f9CwO > div > div > div > div.zp_hpMiB.zp_FAqrS > button.zp-button.zp_zUY3r.zp_n9QPr.zp_rhXT_')))
        Email.click()

        # After clicking the email button, re-locate the Name and Position elements
        Name = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#main-app > div.zp_GhGgo > div.zp_HrbxN > div > div.zp_HrbxN > div:nth-child(1) > div.page-header.zp_yfwnw > div.zp_I8qdp > div.zp_cu0dr > div.zp_MGlfT.zp_IsAWH > div.zp_FvUYj.zp_u83Uf > div > div.zp_gOECT > div > div > div > div:nth-child(1) > div > div > div > div.zp_w0Cv0.zp_EXndU > div.zp_TNVkG.zp_f9CwO > div > div:nth-child(1) > div > div.zp_XtT7n > div.zp__iJHP > div.zp-inline-edit-popover-trigger.zp_oSeJs.zp_YhA6I.zp_cq_5Q > div')))
        Position = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#main-app > div.zp_GhGgo > div.zp_HrbxN > div > div.zp_HrbxN > div:nth-child(1) > div.page-header.zp_yfwnw > div.zp_I8qdp > div.zp_cu0dr > div.zp_MGlfT.zp_IsAWH > div.zp_FvUYj.zp_u83Uf > div > div.zp_gOECT > div > div > div > div:nth-child(1) > div > div > div > div.zp_w0Cv0.zp_EXndU > div.zp_TNVkG.zp_f9CwO > div > div:nth-child(1) > div > div.zp_XtT7n > div.zp_u8xsG.zp_PCMp6.zp_TLkaB > div > div > div.zp_H6PH2 > span.zp_LkFHT')))
        
        Get_Email = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 
            '#main-app > div.zp_GhGgo > div.zp_HrbxN > div > div.zp_HrbxN > div:nth-child(1) > div.page-header.zp_yfwnw > div.zp_I8qdp > div.zp_cu0dr > div.zp_MGlfT.zp_IsAWH > div.zp_FvUYj.zp_u83Uf > div > div.zp_gOECT > div > div > div > div:nth-child(1) > div > div > div > div.zp_w0Cv0.zp_EXndU > div.zp_TNVkG.zp_f9CwO > div > div:nth-child(2) > div > div.zp_WqaMo > div > div:nth-child(1) > div > div.zp_Z99Vh > div > div > div.zp_CMRyD > div > div > div > div > a')))
        time.sleep(1)
        email_text = Get_Email.text
        try:
            Industry = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#location_detail_card > div > div > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div.zp_hYCdb.zp_fleZh > div')))
            Industry = Industry.text
        except TimeoutException:
            Industry = "Industry Not Listed"
            
        except Exception as e:
            print(f"An error occurred while retrieving the industry: {str(e)}")
            Industry = "Industry Not Listed"

        print(f"Email found: {email_text}")
        time.sleep(1)
        new_row = {'Company': company, 'Name': Name.text, 'Position': Position.text, 'Email': email_text, 'Industry':Industry}
        global data
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        return True  # Indicate that a name has been found
    except TimeoutException:
        print("Email button not found, continuing to the next step.")
        return False  # Indicate that no name has been found

keywords = ['Director', 'Business Development', 'Partner', 'Partnership', 'Sales', 'Account Manager']

for company in companies[:]:  # Iterate over a copy of the list to allow modifications
    print(f"Processing company: {company}")
    search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-app > div.zp_GhGgo > div > div > div.zp_HrbxN > div:nth-child(1) > div.page-header.zp_yfwnw > div.zp_I8qdp > div.zp_JjEDk > div > input')))
    search.clear()
    search.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
    search.send_keys(Keys.DELETE)  # Delete all text in the input field
    search.send_keys(company)
    time.sleep(5)

    try:
        FirstCompanyClick = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#omnisearch-container > div > div > div:nth-child(2) > div:nth-child(2)')))
        FirstCompanyClick.click()
        time.sleep(5)

        try:
            PeopleClick = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#insights_card > div > div.zp_TIhxw > div > a:nth-child(3)')))
            PeopleClick.click()
            time.sleep(2)
        except:
            EmployeesClick = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#panel-content-container > div > div.zp_HwbaH > div > div.zp_xh9yN > div > a:nth-child(5)')))
            EmployeesClick.click()
            time.sleep(2)

        name_found = False

        for keyword in keywords:
            if name_found:
                break
            try:
                print(f"Searching for keyword: {keyword}")
                # Use XPATH to search for elements containing the keyword text
                elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(text(), '{keyword}')]")))

                for element in elements:
                    # Get the CSS selector of the found element
                    css_selector = get_css_selector(element)
                    CSSClick = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                    CSSClick.click()
                    time.sleep(3)
                    name_found = ScrapeInfo(company)

                    data.to_csv(r"test13.csv", index=False)

                    if name_found:
                        break

            except Exception as e:
                print(f"An error occurred while searching for keyword '{keyword}': {str(e)}")
                continue

        if not name_found:
            print(f"Could not find enough information for {company}")

    except TimeoutException:
        print(f"Company '{company}' not found. Removing from list.")
        companies.remove(company)
        continue

    except Exception as e:
        print(f"An error occurred while processing company '{company}': {str(e)}")
        continue

print("Ending script.")