import MySQLdb
import time
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from timesjobs import jobs
from pathlib import Path

if __name__ == '__main__':
    #Initialize the database
    try:
        db_jobListings = MySQLdb.connect(
        host='harshdonga.mysql.pythonanywhere-services.com',
        user='harshdonga',
        passwd='Admin@2020',
        db='harshdonga$talentserveDB'
        )
        db = db_jobListings.cursor()
        print("Connected to the database successfully")
    except:
        print("Error occurred when connecting to the database")
        quit()

    with open(f'{Path(__file__).resolve().parent}/job_titles.txt') as inp:
        search_queries = inp.read().split(',')

    #Initialize the driver and url
    session = HTMLSession()

    # try:
    #     db.execute(
    #         'TRUNCATE TABLE home_joblistings'
    #     )
    #     db_jobListings.commit()
    # except Exception as e:
    #     print(f"Unable to truncate table error : {e}")
    #     pass

    # print("Cleared the table")

    for query in search_queries:
        search_query = query[1:-1]
        print('topic - ',search_query)
        base_url = 'https://www.naukri.com/'
        url = base_url + f"{search_query.replace(' ','-')}-jobs?k={search_query}"
        print("Starting the scraper")

        #Searching Naukri.com
        # print("---> On Naukri.com <---")
        # jobUrls = []
        # try:
        #     r = session.get(url)
        #     r.html.render()
        #     soup = BeautifulSoup(r.html.raw_html, 'lxml')
        #     print("On Page 1")
        #     print("Recieved the response for job listings")
        #     job_list = soup.find('div', class_='list')
        #     # Job Link
        #     jb_ls_a = job_list.find_all('a', class_='title fw500 ellipsis')
        #     # Company name
        #     jb_ls_c = job_list.find_all('a',class_='subTitle ellipsis fleft')
        #     jobUrls.extend(list(zip(
        #         [it['data-job-id'] for it in job_list.find_all('article',class_='jobTuple bgWhite br4 mb-8')],
        #         [it['href'] for it in jb_ls_a],
        #         [it['title'] for it in jb_ls_a],
        #         [it['title'] for it in jb_ls_c]
        #     )))
        # except Exception as e:
        #     print(f"Error Occurred : {e}")

        # #Getting More Job listings
        # print("Getting more Job Listings")
        # try:
        #     pages = soup.find('div',class_='fleft pages')
        #     pages = pages.find_all('a')
        # except Exception as e:
        #     print(f"Error : {e}")
        # for page in pages[1:]:
        #     try:
        #         print(f"On Page {page.text}")
        #         #print(base_url+f"{search_query.replace(' ','-')}-jobs-{page.text}?k={search_query.replace(' ','-')}")
        #         url = base_url+f"{search_query.replace(' ','-')}-jobs-{page.text}?k={search_query.replace(' ','-')}"
        #         r = session.get(url)
        #         r.html.render()
        #         soup = BeautifulSoup(r.html.raw_html, 'lxml')
        #         print("Recieved the response for job listings")
        #         job_list = soup.find('div', class_='list')
        #         # Job Link
        #         jb_ls_a = job_list.find_all('a', class_='title fw500 ellipsis')
        #         # Company name
        #         jb_ls_c = job_list.find_all('a',class_='subTitle ellipsis fleft')
        #         jobUrls.extend(list(zip(
        #             [it['data-job-id'] for it in job_list.find_all('article',class_='jobTuple bgWhite br4 mb-8')],
        #             [it['href'] for it in jb_ls_a],
        #             [it['title'] for it in jb_ls_a],
        #             [it['title'] for it in jb_ls_c]
        #         )))
        #     except Exception as e:
        #         print(f"Error Occurred : {e}")
        # print(f"No. of JobUrls = {len(jobUrls)}")

        # #Iterate through all the Job URLs
        # print("Iterating through job URLs")
        # for job_url in jobUrls:
        #     try :
        #         r = session.get(job_url[1])
        #         r.html.render()
        #         soup = BeautifulSoup(r.html.raw_html, 'lxml')
        #         job_id = job_url[0]
        #         job_link = job_url[1]
        #         job_title = job_url[2]
        #         company_name = job_url[3]
        #         job_description = soup.find('div',class_='dang-inner-html').text
        #         job_requirement = ', '.join([it.find('span').text for it in soup.find('div',class_='key-skill').findChildren('a')])
        #         job_location = soup.find('span',class_='location').find('a').text
        #         job_salary = soup.find('div',class_='salary').find('span').text
        #         job_qualification = soup.find('div',class_='education').text
        #         job_type = soup.find('div',class_='other-details').select('div.details:nth-child(4) > span:nth-child(2) > span:nth-child(1)')[0].text
        #         job_experience = soup.find('div', class_='exp').find('span').text
        #     except Exception as e:
        #         print(f"Error - Custom Webpage")
        #         print(f"Job url = {job_link}")
        #         continue
        #     try:
        #         db.execute(
        #             'INSERT INTO home_joblistings (job_id,job_topic,job_link,company_name,job_title,job_description,job_requirements,job_location,job_salary,job_qualification,job_type,job_experience) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        #             (job_id,search_query,job_link,company_name,job_title,job_description,job_requirement,job_location,job_salary,job_qualification,job_type,job_experience,)
        #         )
        #         db_jobListings.commit()
        #     except Exception as e:
        #         print(f"Error Occurred while inserting into the database : {e}")
        #         continue
        #     print("Added successfully")

        #Searching Indeed
        print("---> On Indeed.com <---")
        try:
            jobUrls = []
            url = f"https://in.indeed.com/jobs?q={search_query.replace(' ','+')}&l="
            r = session.get(url)
            r.html.render()
            soup = BeautifulSoup(r.html.raw_html, 'lxml')
            print("On Page 1")
            print("Recieved the response for job listings")
            job_list = soup.find_all('div',class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
            jb_ls_loc = soup.find_all('span',class_='location')
            jb_ls_a = soup.find_all('a',class_='jobtitle turnstileLink')
            jb_ls_c = soup.find_all('span',class_='company')
            jobUrls.extend(list(zip(
                [it['id'] for it in job_list],
                [it['href'] for it in jb_ls_a],
                [it.text.encode('ascii', errors='ignore') for it in jb_ls_a],
                [it.find('span',class_='salaryText').text.encode('ascii', errors='ignore') if it.find('span',class_='salaryText') is not None else 'N/A' for it in job_list],
                [it.text.encode('ascii', errors='ignore') for it in jb_ls_loc],
                [it.find('div',class_='summary').text.encode('ascii', errors='ignore') for it in job_list],
                [it.text.encode('ascii', errors='ignore') for it in jb_ls_c]
            )))
        except Exception as e:
            print(f"Error : {e}")

        #Getting more job listings
        print("Getting more Job Listings")
        try:
            pages = soup.find('ul',class_='pagination-list')
            pages = pages.find_all('span',class_='pn')
            for page in pages[:-1]:
                print(f"On Page {page.text}")
                url = f"https://in.indeed.com/jobs?q={search_query.replace(' ','+')}&start={int(page.text)-1}0"
                r = session.get(url)
                r.html.render()
                soup = BeautifulSoup(r.html.raw_html, 'lxml')
                print("Recieved the response for job listings")
                job_list = soup.find_all('div',class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
                jb_ls_loc = soup.find_all('span',class_='location')
                jb_ls_a = soup.find_all('a',class_="jobtitle turnstileLink")
                jb_ls_c = soup.find_all('span',class_='company')
                jobUrls.extend(list(zip(
                    [it['id'] for it in job_list],
                    [it['href'] for it in jb_ls_a],
                    [it.text.encode('ascii', errors='ignore') for it in jb_ls_a],
                    [it.find('span',class_='salaryText').text.encode('ascii', errors='ignore') if it.find('span',class_='salaryText') is not None else 'N/A' for it in job_list],
                    [it.text.encode('ascii', errors='ignore') for it in jb_ls_loc],
                    [it.find('div',class_='summary').text.encode('ascii', errors='ignore') for it in job_list],
                    [it.text.encode('ascii', errors='ignore') for it in jb_ls_c]
                )))
        except Exception as e:
            print(f"Error : {e}")
        print(f"No. of JobUrls = {len(jobUrls)}")

        #Iterating through jobUrls
        print("Iterating through jobUrls")
        for job_url in jobUrls:
            try:
                r = session.get('https://in.indeed.com/'+job_url[1][1:])
                r.html.render()
                soup = BeautifulSoup(r.html.raw_html,'lxml')
                job_id = job_url[0]
                job_link = job_url[1]
                job_title = job_url[2]
                job_description = soup.find('div',{'id':'jobDescriptionText'}).text.encode('ascii', errors='ignore')
                job_salary = job_url[3]
                job_location=job_url[4]
                job_requirement = job_url[5]
                company_name = job_url[6]
            except Exception as e:
                print(f"Error : {e}")
                continue
            try:
                db.execute(
                    'INSERT INTO home_joblistings (job_id,job_topic,job_link,company_name,job_title,job_description,job_requirements,job_location,job_salary,job_qualification,job_type,job_experience) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (job_id,search_query,job_link,company_name,job_title,job_description,job_requirement,job_location,job_salary,"N/A","N/A","N/A",)
                )
                db_jobListings.commit()
            except Exception as e:
                print(f"Error Occurred while inserting into the database : {e}")
                continue
            print("Added successfully")

        #Searching timesjobs.com
        print("---> On timesjobs.com <---")
        jobUrls = []
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={search_query.replace(' ','%20')}&txtLocation="
        try:
            r = session.get(url)
            r.html.render()
            soup = BeautifulSoup(r.html.raw_html,'lxml')
            print("On Page 1")
            print("Recieved the response for job listings")
            job_list = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
            jb_ls_header = [jb.find('header',class_='clearfix') for jb in job_list]
            jb_ls_a = [jb.find('a') for jb in jb_ls_header]
            jb_ls_c = soup.find_all('h3',class_='joblist-comp-name')
            jobUrls.extend(list(zip(
                [re.search(r"(?<=jobid-)(.+?(?=__))",it['href']).group() for it in jb_ls_a],
                [it['href'] for it in jb_ls_a],
                [it.text.encode('ascii', errors='ignore') for it in jb_ls_a],
                [it.text.encode('ascii', errors='ignore') for it in jb_ls_c]
            )))
        except Exception as e:
            print(f"Error : {e}")

        #Getting more job listings
        print("Getting more Job Listings")
        try:
            pages = soup.find('div',class_='srp-pagination clearfix')
            pages = pages.find_all('a',{'rel':'next'})
        except Exception as e:
            print(f"Error : {e}")
        for page in pages[:-1]:
            try:
                url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords={search_query.replace(' ','%20')}&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords={search_query.replace(' ','%20')}&pDate=I&sequence={page.text}&startPage=1"
                r = session.get(url)
                r.html.render()
                soup = BeautifulSoup(r.html.raw_html,'lxml')
                print(f"On Page {page.text}")
                print("Recieved the response for job listings")
                job_list = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
                jb_ls_header = [jb.find('header',class_='clearfix') for jb in job_list]
                jb_ls_a = [jb.find('a') for jb in jb_ls_header]
                jb_ls_c = soup.find_all('h3',class_='joblist-comp-name')
                jobUrls.extend(list(zip(
                    [re.search(r"(?<=jobid-)(.+?(?=__))",it['href']).group() for it in jb_ls_a],
                    [it['href'] for it in jb_ls_a],
                    [it.text.encode('ascii', errors='ignore') for it in jb_ls_a],
                    [it.text.encode('ascii', errors='ignore') for it in jb_ls_c]
                )))
            except Exception as e:
                print(f"Error : {e}")
        print(f"No. of JobUrls = {len(jobUrls)}")

        #Iterating through jobUrls
        print("Iterating through jobUrls")
        for job_url in jobUrls:
            job_id = job_url[0]
            job_link = job_url[1]
            job_title = job_url[2]
            company_name = job_url[3]
            try:
                (company,
                time_period,
                job_salary,
                job_location,
                job_description,
                job_details,
                job_requirement,
                company_details_dict
                )=jobs(job_url[1])
            except:
                continue
            company_name = company_name.decode('utf-8').encode('ascii', errors='ignore')
            job_salary = job_salary.encode('ascii', errors='ignore')
            job_location = job_location.encode('ascii', errors='ignore')
            job_description = job_description.encode('ascii', errors='ignore')
            job_title = job_title.decode('utf-8').encode('ascii', errors='ignore')

            try:
                db.execute(
                    'INSERT INTO home_joblistings (job_id,job_topic,job_link,company_name,job_title,job_description,job_requirements,job_location,job_salary,job_qualification,job_type,job_experience) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (job_id,search_query,job_link,company_name,job_title,job_description,job_requirement,job_location,job_salary,"N/A","N/A","N/A",)
                )
                db_jobListings.commit()
            except Exception as e:
                print(f"Error Occurred while inserting into the database : {e}")
                continue
            print("Added successfully")
        print(f"Scraper completed for query {search_query}")
    print("Scraping Completed")
