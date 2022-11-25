# import time
# import random
# import os
import time
from random import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# driver_path = input("Enter your downloaded chromedriver filepath, "
#                    "EX: /Users/alexander/Downloads/chromedriver: ")
driver_path = "/Users/alexanderskladanek/Downloads/chromedriver"

# driver = webdriver.Safari()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(driver_path, options=options)

URL_1 = "https://www.linkedin.com/jobs/search?keywords=Software%2BEngineer&" \
        "location=United%2BStates&geoId=103644278&f_E=2&currentJobId=3353722977&position=1&pageNum=0"


def remove_element(passed_in_driver, element):
    # "document.getElementById(\"element_id\");element.remove();"
    string_to_remove = "document.getElementById(\"" + element + "\");element.remove();"
    passed_in_driver.execute_script(string_to_remove)


def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    # scroll_nav_out_of_way = 'window.scrollBy(0, -);'
    passed_in_driver.execute_script(scroll_by_coord)
    # passed_in_driver.execute_script(scroll_nav_out_of_way)


# try:
opened = 0
driver.get(URL_1)
time.sleep(2 + 0.1 * random())
# driver.maximize_window()
driver.maximize_window()
return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
return_sidebar_plus_button = driver.find_element(By.CLASS_NAME, "two-pane-serp-page__results-list")
for i in range(0, 7):
    time.sleep(2 + 0.5 * random())
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
    print("0:", len(job_list))
while len(job_list) < 900:
    time.sleep(2 + 0.5 * random())
    buttonList = return_sidebar_plus_button.find_elements(By.TAG_NAME, "button")
    for b in buttonList:
        if b.text == " See more jobs " or b.text == "See more jobs":
            x = b
    try:
        toasts = driver.find_element(By.ID, "toasts")
        driver.execute_script("return arguments[0].remove();", toasts)
        print("removed toasts")
    except:
        pass
    x.click()
    return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
    print("0.5:", len(job_list))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
# print("Acquired list of search results")
# print(return_sidebar)
job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
print("1:", len(job_list))
for x in job_list:
    # print(x.text)
    # perform title filtering
    if "Associate" in x.text or "Intern" in x.text or "Web" in x.text or "fullstack" in x.text or "Full-Stack" in x.text \
            or "Cloud" in x.text or "System" in x.text or "Windows" in x.text or "Back-End" in x.text or "Backend" in x.text \
            or "back-end" in x.text:
        job_list.remove(x)
print("2:", len(job_list))
i = 0
for x in job_list:
    # print(x.text)
    clicked = False
    try:
        parent_1 = x.find_element(By.XPATH, "./../..")
        scroll_shim(driver, parent_1)
        parent_1.click()
        clicked = True
    except:
        try:
            parent_1 = x.find_element(By.XPATH, "./../../..")

            parent_1.click()
            clicked = True
        except:
            try:
                parent_1 = x.find_element(By.XPATH, "./..")
                parent_1.click()
                clicked = True
            except:
                try:
                    x.click()
                    clicked = True
                except:
                    print("skipped!")
                    pass
    time.sleep(2 + 0.5 * random())
    # Click on each x in job list after filtering
    # filter on number of applicants: num-applicants__caption
    if clicked:
        applicants = driver.find_element(By.CLASS_NAME, "num-applicants__caption")
        if len(applicants.text) > 3:
            if applicants.text[2] == "e" or applicants.text[2].isdigit():
                # removes jobs with "Over 200 applicants" and any with >99 applicants
                job_list.remove(x)
                # print("removed:", applicants.text)
            else:
                parent_1 = x.find_element(By.XPATH, "./..")
                parent_2 = parent_1.find_element(By.XPATH, "./..")
                company = parent_2.find_element(By.CLASS_NAME, "base-search-card__subtitle")
                print(company.text, "|", x.text, "|", applicants.text, "|", parent_1.get_attribute("href"))
                pass
                # print(x.text, applicants.text)
print("3:", len(job_list))
# find globally show-more-less-html__markup show-more-less-html__markup--clamp-after-5
# concatenate all the text paragraphs and break rooms
# use that text to filter out jobs with 1+, 2+, 3+ years of experience
print("All finished, happy hunting!")
# except:
#     # driver.quit()
#     print("Program failed...")

# manage().window().maximize()
# try:
#     driver.find_element_by_id("cross-icon").find_element_by_xpath('..').click()
# except:
#     pass
# hearts = int(input("Please enter the number of hearts you'd like to be the threshold: "))
# i = 0
# tabs = int(input("Please enter the number of tabs you'd like to open: "))
#
#
# def scroll_shim(passed_in_driver, object):
#     x = object.location['x']
#     y = object.location['y']
#     scroll_by_coord = 'window.scrollTo(%s,%s);' % (
#         x,
#         y
#     )
#     # scroll_nav_out_of_way = 'window.scrollBy(0, -);'
#     passed_in_driver.execute_script(scroll_by_coord)
#     # passed_in_driver.execute_script(scroll_nav_out_of_way)
#
#
# page = 1
# while opened < tabs:
#     if len(driver.find_elements_by_class_name("u-font-copy")) <= i:
#         time.sleep(1 + 0.1 * random())
#         print("Checking Next Page!")
#         page += 1
#         driver.get(
#             URL_2_1 + str(page) + URL_2_2)
#         time.sleep(1 + 0.1 * random())
#         if page == 2:
#             time.sleep(1 + 0.1 * random())
#             print("currently closing popups on page 2...")
#             driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/form/div[2]/button[2]').click()
#             time.sleep(1 + 0.1 * random())
#             driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/form/button[2]').click()
#             time.sleep(1 + 0.1 * random())
#         i = 0
#     else:
#         if int(driver.find_elements_by_class_name("u-font-copy")[i].text) >= hearts:
#             print("Found One:", driver.find_elements_by_class_name("u-font-copy")[i].text)
#             time.sleep(2.5 + 0.1 * random())
#             element = driver.find_elements_by_class_name("u-font-copy")[i].find_element_by_xpath('./../../..')
#             print("Element parent:", element.text)
#             scroll_shim(driver, element)
#             ActionChains(driver) \
#                 .key_down(Keys.COMMAND) \
#                 .click(element) \
#                 .key_up(Keys.COMMAND) \
#                 .perform()
#             opened += 1
#             time.sleep(1 + 0.1 * random())
#         i += 1
# check if the attached int(text) is greater than hearts
# open the parents associated link if so in new tab
# time.sleep(1) # Crawl delay = 1
# opened += 1
