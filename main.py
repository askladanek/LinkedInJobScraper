import re
import time
from random import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

driver_path = input("Enter your downloaded chromedriver filepath, EX: /Users/alexander/Downloads/chromedriver: \n")

num_jobs_search = int(input("Please enter the number of jobs to filter through: "))

# Arguments to prevent this from being flagged as a bot
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(driver_path, options=options)

URL_1 = input("Please input the URL for your job search, "
              "EX: https://www.linkedin.com/jobs/software-engineer-jobs?keywords=Software%20Engineer&location=United"
              "%20States&locationId=&geoId=103644278&f_TPR=&f_E=2&f_WT=2&position=1&pageNum=0:\n")

job_title_blacklist = input("Please enter any job title words that you would like to filter out of your search:\n").lower().split()

def remove_element(passed_in_driver, element):
    # Removes an element from the driver's DOM view
    # "document.getElementById(\"element_id\");element.remove();"
    string_to_remove = "document.getElementById(\"" + element + "\");element.remove();"
    passed_in_driver.execute_script(string_to_remove)


def scroll_shim(passed_in_driver, object):
    # Scrolls to an object in the driver's current page
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    passed_in_driver.execute_script(scroll_by_coord)


def get_text_including_children(element):
    return_text = ""
    child_list = []
    for e in element.find_elements(By.XPATH, ".//*"):
        child_list.append(e)
    for e in child_list:
        if e.text:
            return_text += e.text
        for f in e.find_elements(By.XPATH, ".//*"):
            child_list.append(f)

    return return_text


logged_in = False

try:
    opened = 0
    driver.get(URL_1)
    #Todo: In future WebDriverWait can replace these sleeps
    time.sleep(2 + 0.1 * random())
    driver.maximize_window()
    return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    return_sidebar_plus_button = driver.find_element(By.CLASS_NAME, "two-pane-serp-page__results-list")
    job_list = list()
    while len(job_list) < num_jobs_search:
        if len(job_list) < 150:
            # At < 150 jobs, the scraper only has to scroll to add more jobs to the list on the page
            time.sleep(2 + 0.5 * random())
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
            job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
            print("Scrolling to add jobs:", len(job_list))
        else:
            # At > 150 jobs, the scraper has to click the button to add more
            time.sleep(2 + 0.5 * random())
            buttonList = return_sidebar_plus_button.find_elements(By.TAG_NAME, "button")
            for b in buttonList:
                if b.text == " See more jobs " or b.text == "See more jobs":
                    x = b
            try:
                # LinkedIn has a strange "toasts" overlay that interferes with the bot clicking
                toasts = driver.find_element(By.ID, "toasts")
                driver.execute_script("return arguments[0].remove();", toasts)
            except:
                pass
            x.click()
            return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
            job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
            print("Button to add more jobs:", len(job_list))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    # print("Acquired list of search results")
    # print(return_sidebar)
    job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
    print("Final accumulated jobs:", len(job_list))
    to_remove_list = []
    for x in job_list:
        # perform title filtering
        for word in job_title_blacklist:
            if word.lower() in x.text.lower():
                to_remove_list.append(x)
    for x in to_remove_list:
        if x in job_list:
            job_list.remove(x)
    print("Jobs filtered by title:", len(job_list))
    tuple_list = list()
    i = 0
    driver2 = webdriver.Chrome(driver_path, options=options)
    for x in job_list:

        # Clicks on each x in job list after filtering
        try:
            parent_1 = x.find_element(By.XPATH, "./../..")
            scroll_shim(driver, parent_1)
            parent_1.click()
            clicked = True
        except:
            print("Job in list skipped!")
            continue
        time.sleep(2 + 0.5 * random())

        # Gets company Name
        parent_1 = x.find_element(By.XPATH, "./..")
        parent_2 = parent_1.find_element(By.XPATH, "./..")
        company = parent_2.find_element(By.CLASS_NAME, "base-search-card__subtitle")
        # gets job link
        job_link = parent_1.get_attribute("href")
        # gets job description:
        try:
            right_card = driver.find_element(By.CLASS_NAME, "show-more-less-html")
            right_card.find_element(By.CLASS_NAME, "show-more-less-html__button").click()
            job_description = get_text_including_children(right_card)
            # parses job description for experience required in years:
            job_experience_required = -1
            # need to match patterns:
            patterns = [r"(years|year).{0,30}experience.{0,30}\d",
                        r"\d.{0,30}(years|year).{0,30}experience",
                        r"minimum.{0,30}experience.{0,30}\d",
                        r"\d.{0,30}minimum.{0,30}experience",
                        r"minimum.{0,30}\d.{0,30}(years|year)",
                        r"\d.{0,30}(years|year)",
                        r"(years|year).{0,30}\d"]
            for p in patterns:
                pattern = re.compile(p, re.IGNORECASE)
                m = pattern.search(job_description)
                if m:
                    pattern_digit = re.compile(r"\d")
                    job_experience_required = int(pattern_digit.search(m.group()).group())
                    break
        except:
            print("Invalid More Button!", company)
            continue
        # gets company link
        driver2.get(
            driver.find_element(By.CLASS_NAME, "topcard__flavor").find_element(By.TAG_NAME, "a").get_attribute("href"))
        # gets company size
        try:
            time.sleep(3 + 0.5 * random())
            company_info = driver2.find_element(By.CLASS_NAME, "mt1").find_elements(By.XPATH, ".//*")
            company_size = "0"
            for i in company_info:
                if "employees" in i.text:
                    company_size_temp = i.text
                    company_size = ""
                    if "\\n" in company_size_temp or "\n" in company_size_temp:
                        i = 0
                        # getting second digit sometimes means when >9 people from your school/job
                        #   work there, it leads to weird numbers
                        for d in company_size_temp:
                            if i != 0:
                                if d.isdigit():
                                    i += 1
                                    company_size += d
                            else:
                                if d.isdigit():
                                    i += 1
                    else:
                        for d in company_size_temp:
                            if d.isdigit():
                                company_size += d
                    break
        except:
            if not logged_in:
                input("Please log in on the second browser. Hit the Enter key when you are done:")
                logged_in = True
                driver2.get(
                    driver.find_element(By.CLASS_NAME, "topcard__flavor").find_element(By.TAG_NAME, "a").get_attribute(
                        "href"))
                time.sleep(3 + 0.5 * random())
                company_info = driver2.find_element(By.CLASS_NAME, "mt1").find_elements(By.XPATH, ".//*")
                company_size = "0"
                for i in company_info:
                    if "employees" in i.text:
                        company_size_temp = i.text
                        company_size = ""
                        if "\\n" in company_size_temp or "\n" in company_size_temp:
                            i = 0
                            for d in company_size_temp:
                                if i != 0:
                                    if d.isdigit():
                                        i += 1
                                        company_size += d
                                else:
                                    if d.isdigit():
                                        i += 1
                        else:
                            for d in company_size_temp:
                                if d.isdigit():
                                    company_size += d
                        break
            else:
                print("Invalid Company!", company)
                continue
        # gets applicants
        try:
            applicants = driver.find_element(By.CLASS_NAME, "num-applicants__caption")
        except:
            print("No applicant #")
            continue
        tuple_list.append((company.text, company_size, x.text, applicants.text, job_experience_required, job_link))
        print(tuple_list[-1])
    print("Post Info Gathering:", len(tuple_list))
    to_remove_list = []
    company_names = []
    company_names2 = []
    for x in tuple_list:
        # company size filter
        if int(x[1]) < 100:
            to_remove_list.append(x)
            continue
        # applicant number filter
        if len(x[3]) > 3:
            if 'Over 200 applicants' in x[3] or x[3][2].isdigit() or (
                    x[3][0].isdigit() and int(x[3][0]) > 5 and x[3][1].isdigit()):
                # removes jobs with "Over 200 applicants" and any with >59 applicants
                to_remove_list.append(x)
                continue
        # Experience in years filter
        # if x[4] > 2 or x[4] < 0:
        if int(x[4]) > 2:
            to_remove_list.append(x)
            continue
        # removing more than 2 positions from the same company
        if x[0] not in company_names:
            company_names.append(x)
        else:
            if x[0] not in company_names2:
                company_names2.append(x)
            else:
                to_remove_list.append(x)
                continue
    # Remove from list while not iterating over it
    for x in to_remove_list:
        tuple_list.remove(x)
    print("Post Company Size/Applicant Filtering:", len(tuple_list))
    print("All finished, happy job hunting!")
    tuple_list.sort(key=lambda y: y[1])  # sort by company size
    tuple_list.sort(key=lambda y: y[4])  # sort by years of experience
finally:
    # Prints out list even if an error occurred due to computer going to sleep, etc
    for x in tuple_list:
        res = ""
        for y in x:
            res += str(y) + " | "
        # Prints out all elements in the filtered job tuple list
        #   excepting the last 3 chars of " | "
        print(res[0:-3])
    print("Company | Company Size | Job Title | Number of Applicants | Experience Required | Link")
