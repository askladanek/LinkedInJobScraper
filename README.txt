Made by Alex Skladanek

Made using Python 3.10
You should download the latest chrome driver before using.
    https://chromedriver.chromium.org
And put your specific driver download path in the driver_path variable.
You may need to install Selenium before using this script.
    pip install selenium
This web scraper uses Selenium to open two Chrome windows.
Using the URL_1 variable (a link to a job search on LinkedIn,
sourced from a private browser to ensure no login data),
it first scans the left column for job titles, company links, etc.
Next, it opens the company link to gather employee numbers.
You will need to log on in the second browser for this to work.
After logging in, press "Enter" in the console to allow the program to continue.
Then it clicks on each item in the job result list sequentially,
filtering based on the criteria specified in code:

job title- [edit parameter in job_title_blacklist]
minimum years of experience- [edit parameter in max_years_experience]
number of employees- [edit parameter in min_company_size]
number of applicants- [edit the if statement under # applicant number filter]

And then sort first based on company size, then necessary experience.
The code will continue to run until the necessary number of jobs
have been found or the program crashes/stalls. There is various
error correction in the code for if a company has no employee count,
the "See More" button fails to appear on a job description, etc., but
nothing can be done if the program stalls due to your computer going
to sleep. If the program stalls, you can stop it manually, and it
should still sort and print the results.

Possible errors may arise when the windows are resized,
it seems to work fine on 1080p horizontal monitor on Mac.
You may need to change what class the driver searches for
or window sizing if this becomes an issue for you.
If your computer is blazing fast, you may want to add a one-second
+ 0.5*rand delay between job clicks to ensure you're not flagged
for overloading server requests.

A reminder that web scraping publicly accessible information is legal
but LinkedIn tries to make a profit off data, so they make this as
hard as possible and element names/classes may change.

Happy job hunting!