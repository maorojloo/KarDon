
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


def importData2DB(id):
    url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetDetail"
    querystring = {"jobPostId":id}
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
                if res['data']['locations'][0]["country"]['id']:
                    Id = res['data']['locations'][0]["country"]['id']
                if res['data']['locations'][0]["country"]['titleFa']:
                    titleFa  = res['data']['locations'][0]["country"]['titleFa']
                if res['data']['locations'][0]["country"]['titleEn']:
                    titleEn = res['data']['locations'][0]["country"]['titleEn']
            ),
            province = Province(
                if res['data']['locations'][0]["province"]['id']
                    Id = res['data']['locations'][0]["province"]['id']
                if res['data']['locations'][0]["province"]['titleFa']:
                    titleFa  = res['data']['locations'][0]["province"]['titleFa']

                if res['data']['locations'][0]["province"]['titleEn']:
                    titleEn = res['data']['locations'][0]["province"]['titleEn']
            ),
            city = City(
                if res['data']['locations'][0]["city"]['id']
                    Id = res['data']['locations'][0]["city"]['id']
                if res['data']['locations'][0]["city"]['titleFa']
                    titleFa  = res['data']['locations'][0]["city"]['titleFa']
                if res['data']['locations'][0]["city"]['titleEn']
                    titleEn = res['data']['locations'][0]["city"]['titleEn']
            )
        ),
        # Parse this Worktype list and look for the 0 , 1 , ...

        workTypes = WorkTypes(
            if res['data']['workTypes'][0]['id']
                Id = res['data']['workTypes'][0]['id']
            if res['data']['workTypes'][0]['titleFa']
                titleFa  = res['data']['workTypes'][0]['titleFa']
            if res['data']['workTypes'][0]['titleEn']
                titleEn = res['data']['workTypes'][0]['titleEn']

        ),
        if res['data']['salary']
            salary = res['data']['salary']
        if res['data']['normalizeSalaryMin']
            normalize_salary_min = res['data']['normalizeSalaryMin']
        if res['data']['normalizeSalaryMax']
            normalize_salary_max = res['data']['normalizeSalaryMax']
        if res['data']['hasNoWorkExperienceRequirement']
            has_no_work_experience_requirement = res['data']['hasNoWorkExperienceRequirement']
        # Write a Gender Parser
        if res['data']['gender']
            gender = res['data']['gender']
        # Parse This AcademicRequirements list and look for the 0 , 1, ...
        #if res['data']['academicRequirements'][0]:
        academic_requirements = AcademicRequirements(
                if res['data']['academicRequirements'][0]['id']
                    Id = res['data']['academicRequirements'][0]['id']
                if res['data']['academicRequirements'][0]['levelTitle']
                    levelTitle  = res['data']['academicRequirements'][0]['levelTitle']
                if res['data']['academicRequirements'][0]['titleFa']
                    titleFa = res['data']['academicRequirements'][0]['titleFa']
                if res['data']['academicRequirements'][0]['titleEn']
                    titleEn = res['data']['academicRequirements'][0]['titleEn']
            ),
        if res['data']['requiredLanguageSkills']     
            requiredLanguageSkills = res['data']['requiredLanguageSkills']
        if res['data']['requiredWorkExperience']
            required_work_experience = res['data']['requiredWorkExperience']
        if res['data']['skills']
            skills = res['data']['skills']
        requiredEducations = RequiredEducations(
            if res['data']['requiredEducations'][0]["id"]
                id = res['data']['requiredEducations'][0]["id"]
            if res['data']['requiredEducations'][0]["titleFa"]
                titleFa = res['data']['requiredEducations'][0]["titleFa"]
            if res['data']['requiredEducations'][0]["titleEn"]
                titleEn = res['data']['requiredEducations'][0]["titleEn"]
        ),
        if res['data']['militaryServiceState']
            military_service_state =  res['data']['militaryServiceState']
        if res['data']['isInternship']
            is_internship = res['data']['isInternship']
        if res['data']['hasAlternativeMilitary']
            has_alternative_military = res['data']['hasAlternativeMilitary']
        if res['data']['isRemote']
            is_remote = res['data']['isRemote']
        if res['data']['hasInsurance']
            hasInsurance = res['data']['hasInsurance']
        if res['data']['paymentMethod']
            paymentMethod = res['data']['paymentMethod']
        if res['data']['workHours']
            workHours = res['data']['workHours']
        if res['data']['seniorityLevel']
            seniorityLevel=res['data']['seniorityLevel']
        publishTime = ActivationTime(
            # passedDays = res['data']['publishTime']['passedDays'],
            # beautifyFa = res['data']['publishTime']['beautifyFa'],
            # beautifyEn = res['data']['publishTime']['beautifyEn'],
            if res['data']['publishTime']['date']
                date = res['data']['publishTime']['date']
        ),
        if res['data']['benefits']
            benefits = res['data']['benefits']
        if res['data']['requiredKnowledge']           
            requiredKnowledge = res['data']['requiredKnowledge']
        if res['data']['businessTripsDescription']
            businessTripsDescription = res['data']['businessTripsDescription']
        if res['data']['minAge']
            minAge = res['data']['minAge'] 
        if res['data']['maxAge']
            maxAge = res['data']['maxAge']
        if res['data']['softwareSkills']
            softwareSkills = res['data']['softwareSkills']
        if res['data']['labels']
            labels = res['data']['labels']

        expireTime = ExpireTime(
            if res['data']['expireTime']['date']
                date = res['data']['expireTime']['date']
            # days_left_until = res['data']['expireTime']['daysLeftUntil']
        ),
        if res['data']['isExpired']
            is_expired =  res['data']['isExpired']
        if res['data']['contactInfo']
            contactInfo = res['data']['contactInfo']
        # This fields needs a lot more to look!
        #jobPostCategories = res['data']['jobPostCategories'],
        job_board = JobBoard(
            if res['data']['jobBoard']['organizationColor']
                organizationColor = res['data']['jobBoard']['organizationColor']
            if res['data']['jobBoard']['id'] 
                Id = res['data']['jobBoard']['id'] 
            if res['data']['jobBoard']['titleFa']
                titleFa = res['data']['jobBoard']['titleFa']
            if res['data']['jobBoard']['titleEn'] 
                titleEn = res['data']['jobBoard']['titleEn'] 
        )
        )



    elastic_id = new_instance.save(refresh=True)
    print(elastic_id)




jobPostIds = redis_client.keys('*')
jobPostIds_not_added = [key.decode('utf-8') for key in jobPostIds if redis_client.get(key) == b'0']
for jobid in jobPostIds_not_added:
    importData2DB(jobid)
    redis_client.set(jobid, 1)

