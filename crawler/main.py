from models import (NormalDoc, Company, CompanyInfo, Province, City, Country, Location,  WorkTypes, JobBoard, ActivationTime, AcademicRequirements, RequiredEducations, ExpireTime,  JobPost)
import requests
import redis
#from config import redis_auth  
import math
from multiprocessing import Pool
import logging
import time


redis_client = redis.Redis(host='localhost', port=6379, password='kardon!!213',  db=0)
logging.basicConfig(filename='app.log', level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')

def paginationinfo():
    url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetList"

    payload = {
        "isInternship": False,
        "isRemote": False,
        "location": None,
        "publishDate": None,
        "workType": None,
        "pageSize": 100,
        "page": 5,
        "sort": 0,
        "JobPostCategories": [],
        "jobBoardIds": []
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)
    
    return {'jobPostCount':response.json()['data']['jobPostCount'],'pageSize':response.json()['data']['pageSize'],}

def collectJobId(page,sendtime=0):
    print('collectJobId is running page  '+str(page))
    url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetList"

    payload = {
        "isInternship": False,
        "isRemote": False,
        "location": None,
        "publishDate": None,
        "workType": None,
        "pageSize": 100,
        "page": page,
        "sort": 0,
        "JobPostCategories": [],
        "jobBoardIds": []
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
    except Exception as e:
        print("can't retries exceeded with url")
        logging.exception("An exception occurred: %s", str(e))


    try:
        if sendtime:
            print("########################################")
            print("fixed in secned time")
            print("########################################")
            
        jobs=response.json()['data']['jobPosts']
        for job in jobs:
            redis_client.setnx(job["id"], 0)

        #raise ValueError("An error occurred!")
    except Exception as e:
        print("============================================")
        logging.exception("An exception occurred: %s", str(e))
        print(str(response.json()))
        print(str(response.status_code))
        if sendtime:
            print("faild in secned time")
        print("============================================")
        #try to collect agin
        if not sendtime:
            collectJobId(page,sendtime=1)

def partition_array(array, n):
    array_size = len(array)
    partition_size = array_size // n
    remainder = array_size % n

    partitions = []
    start = 0

    for i in range(n):
        partition_length = partition_size + (1 if i < remainder else 0)
        end = start + partition_length
        partitions.append(array[start:end])
        start = end

    return partitions
       
def crawldata():
    paginationinformation=paginationinfo()
    count=paginationinformation['jobPostCount']
    pageSize=paginationinformation['pageSize']
    lastPage=math.ceil(count/pageSize)

    page=list(range(1,lastPage))
    #print(page)
    partition_arrys=partition_array(page,50)
    print(partition_arrys)
    print("partition_arrys  "+str(len(partition_arrys)))
    for pageArrys in partition_arrys:
        with Pool(7) as p:
            print("partion number "+str(partition_arrys.index(pageArrys)))
            p.starmap(collectJobId, zip(pageArrys))
        print("sleep to net pation")
        time.sleep(20)
        
def importData2DB(id):
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
        url = res['data']['company']['url'], 
    )

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
            # passedDays = res['data']['publishTime']['passedDays'], 
            # beautifyFa = res['data']['publishTime']['beautifyFa'], 
            # beautifyEn = res['data']['publishTime']['beautifyEn'], 
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
            # days_left_until = res['data']['expireTime']['daysLeftUntil']
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





#IM THE DOC
crawldata()

jobPostIds = redis_client.keys('*')
jobPostIds_not_added = [key.decode('utf-8') for key in jobPostIds if redis_client.get(key) == b'0']
for jobid in jobPostIds_not_added:
    importData2DB(jobid)
    redis_client.set(jobid, 1)


























































# def str2bool(v):
#   return v.lower() in ("yes", "true", "t", "1")


# def getAndAddJobDetail(jobPostId,url):
#     url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetDetail"
#     querystring = {"jobPostId":jobPostId}
#     payload = ""
#     response = requests.request("GET", url, data=payload, params=querystring)

    
#     new_instance = JobDetail(
#         user_id = response.json()['data']['id'],
#         url = response.json()['data']['url'],
#         title = response.json()['data']['title'],
#         description= response.json()['description'],
#         companynametitleFa= response.json()['data']['company']['name']['titleFa'],
#         companylogo =response.json()['data']['logo'],
#         #locations =response.json()['data'],
#         #workTypes = response.json()['data'],
#         hasWorkExperienceRequirement =str2bool(response.json()['data']['hasWorkExperienceRequirement'])? "بدون سابقه کار":"نیاز به سابقه کار",
#         hasAlternativeMilitary = str2bool(response.json()['data']['hasAlternativeMilitary'])? "بدون نیاز به معافیت":"نیاز به معافیت",
#         #benefits = response.json()['data'],
#         seniorityLevel=response.json()['data']['seniorityLevel'],
#         publishTimedate = response.json()['data']['publishTime']['date'],
#         jobBoardorganizationColor = response.json()['data']['jobBoard']['organizationColor'],
#         jobBoardtitleFa = response.json()['data']['jobBoard']['titleFa'],
#         jobBoardtitleEn = response.json()['data']['jobBoard']['titleEn'],
#         companyDetailsSummarynametitleFa = response.json()['data']['companyDetailsSummary']['name']['titleFa']
#         )
    
    
#     session.add(new_instance)
#     session.commit()



















# session.close()