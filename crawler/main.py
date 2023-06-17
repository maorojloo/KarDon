#sqlalchemy modules
# import sqlalchemy as db
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#etc
import requests
import math
from multiprocessing import Pool
import numpy as np
#my modules
# from models import Job,JobDetail



# dburl='sqlite:///kardon.db'
# engine = create_engine(dburl)

# Session = sessionmaker(bind=engine)
# session = Session()

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

    
iasdadasd=1
def collectJobId(page):
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

    response = requests.request("POST", url, json=payload, headers=headers)
    try:
        jobs=response.json()['data']['jobPosts']
        responseArry=[]
        for job in jobs:
            jobinfo=[job["id"],job["url"]]
            responseArry.append(jobinfo)
            
        return responseArry 
    except:
        pass




def crawldata():
    paginationinformation=paginationinfo()
    count=paginationinformation['jobPostCount']
    pageSize=paginationinformation['pageSize']
    result=[]
    lastPage=math.ceil(count/pageSize)
    page=list(range(1,lastPage))
    print(page)
    with Pool(7) as p:
        print("MEWwww")
        for list100 in p.starmap(collectJobId, zip(page)):
            result+=list100

    np.save('my_result.npy', result)
    print(result)


        


crawldata()
# print(collectJobId(10))

























































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