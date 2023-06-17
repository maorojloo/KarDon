#sqlalchemy modules
#import sqlalchemy as db
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from models import (NormalDoc, Company, CompanyInfo, Province, City, Country, Location,  WorkTypes, 
                    JobBoard, ActivationTime, AcademicRequirements, RequiredEducations, ExpireTime,  JobPost)
#etc
import requests
import redis
from config import redis_auth  
r = redis.Redis(host='localhost', port=6379, password=redis_auth, db=0)





def getList():
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
            _id=job['id']
            url=job['url']
            #print("job number "+str(i)+" job id is "+str(id)+" url is ")
            try:
                r.set(_id, url)
                print(_id, url)
            except:
                print("failed to set in redis")
    else:
        # Request failed
        print("Request failed with status code:", response.status_code)




#getList()

def str2bool(v: str):
    return False or v.lower() in ("yes", "true", "t", "1")

def getAndAddJobDetail(jobPostId,url):
    url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetDetail"
    querystring = {"jobPostId":jobPostId}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)
    res = response.json()
    new_company_instance = Company(
        titleFa= res['data']['company']['name']['titleFa'],
        titleEn= res['data']['company']['name']['titleEn'],
        company_logo =res['data']['companyDetailsSummary']['logo'],
        Id = res['data']['companyDetailsSummary']['id'] ,
        description = NormalDoc(
            titleFa = res['data']['company']['description']['titleEn'], 
            titleEn = res['data']['company']['description']['titleEn'], 
        ),
        hasPicture = res['data']['company']['hasPicture'], 
        url = res['data']['company']['url'], 
        job_posts = res['data']['companyDetailsSummary']['jobPosts'],
        job_post_count = res['data']['companyDetailsSummary']['jobPostCount'],
    )
    #print(res['data']['locations'][0]["province"]['id'])
    #print()
    new_instance = JobPost(
        Id = res['data']['id'],
        sourceId = res['data']['sourceId'],
        title = res['data']['title'],
        url = res['data']['url'],
        # This has html tags in it needs to be cleaned :)
        description= res['data']['description'],
        # Make sure description_clean is persian 
        description_clean = res['data']['description'],
        company_info = CompanyInfo(
            name_fa = res['data']['company']['name']['titleFa'],
            name_en = res['data']['company']['name']['titleEn'],
            about = NormalDoc(
                titleFa =   res['data']['companyDetailsSummary']['about']['titleEn'],
                titleEn =  res['data']['companyDetailsSummary']['about']['titleEn'],
            )
        ),
        is_persian = res['data']['isPersian'],
        # Parse this location list and look for the 0 , 1 , ... 
        
        locations = Location(
            country = Country(
                Id = res['data']['locations'][0]["country"]['id'],
                titleFa  = res['data']['locations'][0]["country"]['titleFa'],
                titleEn = res['data']['locations'][0]["country"]['titleEn'],
            ),
            province = Province(
                Id = res['data']['locations'][0]["province"]['id'],
                titleFa  = res['data']['locations'][0]["province"]['titleFa'],
                titleEn = res['data']['locations'][0]["province"]['titleEn'],
            ),
            city = City(
                Id = res['data']['locations'][0]["city"]['id'],
                titleFa  = res['data']['locations'][0]["city"]['titleFa'],
                titleEn = res['data']['locations'][0]["city"]['titleEn'],
            )
        ),
        # Parse this Worktype list and look for the 0 , 1 , ... 

        workTypes = WorkTypes(
            Id = res['data']['workTypes'][0]['id'],
            titleFa  = res['data']['workTypes'][0]['titleFa'],
            titleEn = res['data']['workTypes'][0]['titleEn']
            
        ),
        salary = res['data']['salary'],
        normalize_salary_min = res['data']['normalizeSalaryMin'], 
        normalize_salary_max = res['data']['normalizeSalaryMax'], 
        has_no_work_experience_requirement = res['data']['hasNoWorkExperienceRequirement'],
        # Write a Gender Parser 
        gender = res['data']['gender'], 
        # Parse This AcademicRequirements list and look for the 0 , 1, ...
        #if res['data']['academicRequirements'][0]:
        academic_requirements = AcademicRequirements(
                Id = res['data']['academicRequirements'][0]['id'], 
                levelTitle  = res['data']['academicRequirements'][0]['levelTitle'], 
                titleFa = res['data']['academicRequirements'][0]['titleFa'],
                titleEn = res['data']['academicRequirements'][0]['titleEn'],
            ),
        requiredLanguageSkills = res['data']['requiredLanguageSkills'],
        required_work_experience = res['data']['requiredWorkExperience'],
        skills = res['data']['skills'], 
        requiredEducations = RequiredEducations(
            Id = res['data']['requiredEducations'][0]["id"], 
            titleFa = res['data']['requiredEducations'][0]["titleFa"], 
            titleEn = res['data']['requiredEducations'][0]["titleEn"]
        ), 
        military_service_state =  res['data']['militaryServiceState'], 
        is_internship = res['data']['isInternship'],  
        has_alternative_military = res['data']['hasAlternativeMilitary'],
        is_remote = res['data']['isRemote'],
        hasInsurance = res['data']['hasInsurance'], 
        paymentMethod = res['data']['paymentMethod'], 
        workHours = res['data']['workHours'], 
        seniorityLevel=res['data']['seniorityLevel'],
        publishTime = ActivationTime(
            passedDays = res['data']['publishTime']['passedDays'], 
            beautifyFa = res['data']['publishTime']['beautifyFa'], 
            beautifyEn = res['data']['publishTime']['beautifyEn'], 
            date = res['data']['publishTime']['date'], 
        ),
        benefits = res['data']['benefits'],
        requiredKnowledge = res['data']['requiredKnowledge'],
        businessTripsDescription = res['data']['businessTripsDescription'],
        minAge = res['data']['minAge'] ,
        maxAge = res['data']['maxAge'],
        softwareSkills = res['data']['softwareSkills'],
        labels = res['data']['labels'],
        expireTime = ExpireTime(
            date = res['data']['expireTime']['date'], 
            days_left_until = res['data']['expireTime']['daysLeftUntil']
        ), 
        is_expired =  res['data']['isExpired'],  
        contactInfo = res['data']['contactInfo'], 
        # This fields needs a lot more to look!
        #jobPostCategories = res['data']['jobPostCategories'], 
        job_board = JobBoard(
            organizationColor = res['data']['jobBoard']['organizationColor'], 
            Id = res['data']['jobBoard']['id'] , 
            titleFa = res['data']['jobBoard']['titleFa'], 
            titleEn = res['data']['jobBoard']['titleEn'] , 
        )
        )
    elastic_id = new_instance.save(refresh=True)
    print(elastic_id)

for i in r.keys("*"):
    try: 
        getAndAddJobDetail(i.decode('utf-8'), r.get(i).decode('utf-8'))    
    except: 
        print("SHIT")