import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

num_jobs_search = int(input("Please enter the number of jobs to search for: "))

driver_path = "/Users/your_name_here/Downloads/chromedriver"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(driver_path, options=options)

# URL Breakdown as shown below
# URL_1 = "https://www.linkedin.com/jobs/search?keywords=" \
#         Job Titles, in order of preference
#         "iOS%20Engineer%20" \
#         "OR%20iOS%20Developer%20" \
#         "OR%20Software%20Engineer%20" \
#         "OR%20Mobile%20Developer%20" \
#         "OR%20Mobile%20Engineer%20" \
#         "OR%20Python%20Developer%20" \
#         "OR%20New%20Grad%20" \
#         "OR%20Recent%20Grad" \
#         Location
#         "&location=United%20States&geoId=103644278" \
#         Tracking information
#         "&trk=public_jobs_jobs-search-bar_search-submit" \
#         "&position=1&pageNum=0" \
#         "&refresh=true&sortBy=DD"

URL_1 = "https://www.linkedin.com/jobs/search?keywords=IOS%20Engineer%20OR%20IOS%20Developer%20OR%20Software%20Engineer%20OR%20Mobile%20Developer%20OR%20Mobile%20Engineer%20OR%20Python%20Developer%20OR%20New%20Grad%20OR%20Recent%20Grad&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&position=1&pageNum=0"


def document_initialised(driver):
    return driver.execute_script("return initialised")


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


first = True


def accumulate_jobs(jobs_to_add, num_total_jobs):
    # Accumulate Job Search Results
    return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    global first
    if not first:
        prev_job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
    else:
        prev_job_list = list()
        first = False
    job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
    return_sidebar_plus_button = driver.find_element(By.CLASS_NAME, "two-pane-serp-page__results-list")
    offset = jobs_to_add + len(prev_job_list)
    while len(job_list) < offset:
        exception_happened = False
        job_list_temp_len = len(job_list)
        while len(job_list) < offset and not exception_happened:
            try:
                WebDriverWait(driver, timeout=15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, timeout=15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete")
                return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
                job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
                print("Scrolling to add jobs:", len(job_list))
                if job_list_temp_len == len(job_list):
                    exception_happened = True
                job_list_temp_len = len(job_list)
            except:
                exception_happened = True
        while len(job_list) < offset:
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
            buttonList = return_sidebar_plus_button.find_elements(By.TAG_NAME, "button")
            for b in buttonList:
                if b.text == "See more jobs":
                    x = b
            try:
                toasts = driver.find_element(By.ID, "toasts")
                driver.execute_script("return arguments[0].remove();", toasts)
            except:
                pass
            try:
                x.click()
                return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
                job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
                print("Button Clicked to add more jobs:", len(job_list))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                continue
    return_sidebar = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
    job_list = return_sidebar.find_elements(By.CLASS_NAME, "sr-only")
    for x in prev_job_list:
        if x in job_list:
            job_list.remove(x)
    return job_list


logged_in = False
current_job_num = 0

try:
    opened = 0

    # Initialize Window
    driver.get(URL_1)
    WebDriverWait(driver, timeout=15).until(lambda d: d.execute_script("return document.readyState") == "complete")
    driver.maximize_window()

    job_list = list()

    # Collect Job Information
    tuple_list = list()
    driver2 = webdriver.Chrome(driver_path, options=options)

    while len(tuple_list) < num_jobs_search:
        job_list = accumulate_jobs(20, current_job_num)
        for x in job_list:
            if len(tuple_list) >= num_jobs_search:
                break;
            try:
                # Click on job in left side list
                parent_1 = x.find_element(By.XPATH, "./../..")
                scroll_shim(driver, parent_1)
                parent_1.click()
                clicked = True
            except:
                print("skipped!")
                continue
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
            # Click on each x in job list

            # Gets company Name
            parent_1 = x.find_element(By.XPATH, "./..")
            parent_2 = parent_1.find_element(By.XPATH, "./..")
            company = parent_2.find_element(By.CLASS_NAME, "base-search-card__subtitle")
            if "Diverse Lynx" in company.text:
                continue

            # gets job link
            job_link = parent_1.get_attribute("href")

            # gets company link (for employee count)
            # loads here to decrease time required to wait later
            try:
                WebDriverWait(driver, timeout=15).until(
                    element_to_be_clickable(
                        (By.CLASS_NAME, "topcard__flavor")
                    )
                )
                top_card = driver.find_element(By.CLASS_NAME, "topcard__flavor")
                company_link = top_card.find_element(By.TAG_NAME, "a").get_attribute("href")
                driver2.get(company_link)
            except:
                try:
                    WebDriverWait(driver, timeout=15).until(
                        lambda d: d.execute_script("return document.readyState") == "complete")
                    WebDriverWait(driver2, timeout=15).until(
                        lambda d: d.execute_script("return document.readyState") == "complete")
                    top_card = driver.find_element(By.CLASS_NAME, "topcard__flavor")
                    company_link = top_card.find_element(By.TAG_NAME, "a").get_attribute("href")
                    driver2.get(company_link)
                except:
                    print("Company link Failed to Load!")
                    continue

            # gets job description:
            try:
                right_card = driver.find_element(By.CLASS_NAME, "show-more-less-html")
                right_card.find_element(By.CLASS_NAME, "show-more-less-html__button").click()
                job_description = get_text_including_children(right_card)
                # print(job_description)
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
                print("Bad See More Button!", company)
                continue

            # gets company size
            try:
                WebDriverWait(driver2, timeout=15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete")
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
            except:
                if not logged_in:
                    input("Please log in on the second browser. Hit the Enter key when you are done:")
                    logged_in = True
                    driver2.get(
                        driver.find_element(By.CLASS_NAME, "topcard__flavor").find_element(By.TAG_NAME,
                                                                                           "a").get_attribute(
                            "href"))
                    WebDriverWait(driver2, timeout=15).until(
                        lambda d: d.execute_script("return document.readyState") == "complete")
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
                    print("Bad Company!", company)
                    continue

            # gets applicants
            try:
                applicants = driver.find_element(By.CLASS_NAME, "num-applicants__caption")
            except:
                print("no applicant #")
                continue
            tuple_list.append((company.text, company_size, x.text, applicants.text, job_experience_required, job_link))

            # Filters Through Job Results

            # Company Size Filter
            min_company_size = 100
            if int(tuple_list[-1][1]) < min_company_size:
                tuple_list.remove(tuple_list[-1])
            else:
                # applicant number filter
                if len(tuple_list[-1][3]) > 3 and (
                        'Over 200 applicants' in tuple_list[-1][3] or
                        tuple_list[-1][3][2].isdigit() or (
                        tuple_list[-1][3][0].isdigit() and
                        int(tuple_list[-1][3][0]) > 5 and
                        tuple_list[-1][3][1].isdigit())):
                    # removes jobs with "Over 200 applicants" and any with >59 applicants
                    tuple_list.remove(tuple_list[-1])
                else:
                    # Experience in years filter
                    max_years_experience = 2
                    if int(tuple_list[-1][4]) > max_years_experience:
                        tuple_list.remove(tuple_list[-1])
                    else:
                        # Filter Jobs By Title
                        job_title_blacklist = ["Sr.", "Senior", "III", "Intern", "Web", "fullstack", "Full-Stack",
                                               "Full Stack", "Cloud",
                                               "System", "Windows", "Back-End", "Backend", "Volunteer"]
                        to_remove = False
                        for word in job_title_blacklist:
                            if word.lower() in tuple_list[-1][2].lower():
                                to_remove = True
                                break
                        if to_remove:
                            tuple_list.remove(tuple_list[-1])
                        else:
                            print(str(len(tuple_list)) + "/" + str(num_jobs_search) + ": ", tuple_list[-1])
            current_job_num += 1
            # print(current_job_num)
    print("Post Info Gathering/Filtering:", len(tuple_list))


finally:
    try:
        print(tuple_list)
        print("All finished, happy hunting!")
        # sort by company size
        tuple_list.sort(key=lambda y: y[1])

        # sort by years of experience
        tuple_list.sort(key=lambda y: y[4])
    except:
        pass
    print("Hit Rate:", len(tuple_list) / current_job_num)

    # Print Final Filtered Job List Elements
    for x in tuple_list:
        res = ""
        for y in x:
            res += str(y) + " | "
        print(res[0:-3])
