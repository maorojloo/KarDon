
from models import (NormalDoc, Company, CompanyInfo, Province, City, Country, Location,  WorkTypes, JobBoard, ActivationTime, AcademicRequirements, RequiredEducations, ExpireTime,  JobPost)
import requests
import redis
#from config import redis_auth
import math
from multiprocessing import Pool
import logging
import time
import json



example_json = {
	"data": {
		"id": "",
		"sourceId": "",
		"title": "",
		"url": "",
		"description": "",
		"isPersian": "",
		"company": {
			"name": {
				"titleFa": "",
				"titleEn": ""
			},
			"description": {
				"titleFa": "",
				"titleEn": ""
			},
			"hasPicture": "",
			"logo": "",
			"url": ""
		},
		"locations": [
			{
				"province": {
					"id": "",
					"titleFa": "",
					"titleEn": ""
				},
				"city": {
					"id": "",
					"titleFa": "",
					"titleEn": ""
				},
				"country": {
					"id": "",
					"titleFa": "",
					"titleEn": ""
				}
			}
		],
		"workTypes": [
			{
				"id": "",
				"titleFa": "",
				"titleEn": ""
			}
		],
		"salary": "",
		"normalizeSalaryMin": "",
		"normalizeSalaryMax": "",
		"gender": "",
		"academicRequirements": [
			{
				"levelTitle": "",
				"id": "",
				"titleFa": "",
				"titleEn": ""
			}
		],
		"requiredLanguageSkills": "",
		"skills": "",
		"requiredWorkExperience": "",
		"hasNoWorkExperienceRequirement": "",
		"requiredEducations": [
			{
				"id": "",
				"titleFa": "",
				"titleEn": ""
			}
		],
		"militaryServiceState": "",
		"isInternship": "",
		"hasAlternativeMilitary": "",
		"isRemote": "",
		"hasInsurance": "",
		"paymentMethod": "",
		"workHours": "",
		"seniorityLevel": "",
		"benefits": "",
		"requiredKnowledge": "",
		"businessTripsDescription": "",
		"minAge": "",
		"maxAge": "",
		"softwareSkills": "",
		"labels": [],
		"userInfo": {
			"isBookmarked": ""
		},
		"publishTime": {
			"passedDays": "",
			"beautifyFa": "",
			"beautifyEn": "",
			"date": ""
		},
		"expireTime": {
			"date": "",
			"daysLeftUntil": ""
		},
		"isExpired": "",
		"jobBoard": {
			"organizationColor": "",
			"id": "",
			"titleFa": "",
			"titleEn": ""
		},
		"contactInfo": "",
		"jobPostCategories": "",
		"companyDetailsSummary": {
			"id": "",
			"name": {
				"titleFa": "",
				"titleEn": ""
			},
			"about": {
				"titleFa": "",
				"titleEn": ""
			},
			"logo": "",
			"url": "",
			"jobPosts": "",
			"jobPostCount": ""
		}
	},
	"isSuccess": "",
	"statusCode": "",
	"message": ""
}



redis_client = redis.Redis(host='localhost', port=6379, password='kardon!!213',  db=0)
logging.basicConfig(filename='app.log', level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')

def fill_missing_values(json_obj, example_obj):
    for key in example_obj:
        if key not in json_obj:
            json_obj[key] = example_obj[key]
        elif isinstance(example_obj[key], dict) and isinstance(json_obj[key], dict):
            fill_missing_values(json_obj[key], example_obj[key])

def replace_none_with_empty(json_obj):
    if isinstance(json_obj, dict):
        return {k: replace_none_with_empty(v) if v is not None else "" for k, v in json_obj.items()}
    elif isinstance(json_obj, list):
        return [replace_none_with_empty(elem) if elem is not None else "" for elem in json_obj]
    else:
        return json_obj

def remove_nested_none_dicts(d):
    for k, v in list(d.items()):
        if isinstance(v, dict):
            remove_nested_none_dicts(v)
        if not v:
            del d[k]
    return d


def importData2DB(id):
    url = "https://api.karbord.io/api/v1/Candidate/JobPost/GetDetail"
    querystring = {"jobPostId":id}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)
    print("$$$$$$$$$$$$$$$$$$$$")
    print(id)
    print("$$$$$$$$$$$$$$$$$$$$")

    orginaljson=response.json()
    orginaljson_removedNone=remove_nested_none_dicts(orginaljson)
    res=example_json.update(orginaljson_removedNone)






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




jobPostIds = redis_client.keys('*')
jobPostIds_not_added = [key.decode('utf-8') for key in jobPostIds if redis_client.get(key) == b'0']
for jobid in jobPostIds_not_added:

    importData2DB(jobid)
    print(str(jobid)+" added")

    redis_client.set(jobid, 1)
