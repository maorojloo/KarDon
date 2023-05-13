#sqlalchemy modules
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#etc
import requests

#my modules
from models import Job,JobDetail

dburl='sqlite:///kardon.db'
engine = create_engine(dburl)

Session = sessionmaker(bind=engine)
session = Session()





url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetList"

payload = "{\n  \"isInternship\": false,\n  \"isRemote\": false,\n  \"location\": null,\n  \"publishDate\": null,\n  \"workType\": null,\n  \"pageSize\": 5000,\n  \"page\": 1,\n  \"sort\": 0,\n  \"nextPageToken\": \"{\\\"lastJobPostTime\\\":\\\"2023-05-13T09:50:36.993\\\"}\",\n  \"searchId\": null,\n  \"JobPostCategories\": [\n    \"all-Programming\",\n    \"cto\",\n    \"developer\",\n    \"backend-developer\",\n    \"frontend-developer\",\n    \"node-js-developer\",\n    \"php-developer\",\n    \"wordpress-developer\",\n    \"dot-net-developer\",\n    \"vue-js-developer\",\n    \"full-stack-developer\",\n    \"react-developer\",\n    \"python-developer\",\n    \"java-developer\",\n    \"tech-lead\",\n    \"android-developer\",\n    \"ios-developer\",\n    \"flutter-developer\",\n    \"angular-developer\",\n    \"go-developer\",\n    \"c-developer\",\n    \"dba\"\n  ],\n  \"jobBoardIds\": []\n}"
headers = {'content-type': 'application/json'}
response = requests.post(url, data=payload, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    print("Request was successful.")
    print("Total jobPostCount:", response.json()['data']['jobPostCount'])
    jobs=response.json()['data']['jobPosts']
    for job in jobs:
        id=job['id']
        url=job['url']
        #print("job number "+str(i)+" job id is "+str(id)+" url is ")
        new_instance = Job(id=id, url=url)
        session.add(new_instance)
        session.commit()
        
        getAndAddJobDetail(id,url)
        
        

else:
    # Request failed
    print("Request failed with status code:", response.status_code)




def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def getAndAddJobDetail(jobPostId,url):
    url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetDetail"
    querystring = {"jobPostId":jobPostId}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)

    
    new_instance = JobDetail(
        user_id = response.json()['data']['id'],
        url = response.json()['data']['url'],
        title = response.json()['data']['title'],
        description= response.json()['description'],
        companynametitleFa= response.json()['data']['company']['name']['titleFa'],
        companylogo =response.json()['data']['logo'],
        #locations =response.json()['data'],
        #workTypes = response.json()['data'],
        hasWorkExperienceRequirement =str2bool(response.json()['data']['hasWorkExperienceRequirement'])? "بدون سابقه کار":"نیاز به سابقه کار",
        hasAlternativeMilitary = str2bool(response.json()['data']['hasAlternativeMilitary'])? "بدون نیاز به معافیت":"نیاز به معافیت",
        #benefits = response.json()['data'],
        seniorityLevel=response.json()['data']['seniorityLevel'],
        publishTimedate = response.json()['data']['publishTime']['date'],
        jobBoardorganizationColor = response.json()['data']['jobBoard']['organizationColor'],
        jobBoardtitleFa = response.json()['data']['jobBoard']['titleFa'],
        jobBoardtitleEn = response.json()['data']['jobBoard']['titleEn'],
        companyDetailsSummarynametitleFa = response.json()['data']['companyDetailsSummary']['name']['titleFa']
        )
    
    
    session.add(new_instance)
    session.commit()



















session.close()