import os
from git import Repo
import shutil


repo_url = 'https://github.com/tajrobe/tajrobe.github.io.git'
current_file_path = str(os.path.dirname(__file__)+'/tajrobe-repo')


redis_client = redis.Redis(host='localhost', port=6379, password='kardon!!213',  db=1)

def clone_repository(repo_url, current_file_path):
   try:
      Repo.clone_from(repo_url, current_file_path)
   except:
      if os.path.exists(current_file_path):
         shutil.rmtree(current_file_path)
      Repo.clone_from(repo_url, current_file_path)


def get_folders_in_directory(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

def get_files_in_directory(directory):
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            files.append(item)
    return files

# clone_repository(repo_url, current_file_path)

reviews_path=current_file_path+'/_data/review/'
companys_list = get_folders_in_directory(reviews_path)

for company in companys_list:
   company_review_path=reviews_path+company
   files=get_files_in_directory(company_review_path)

   for fileName in files:
      filePath=company_review_path+"/"+fileName
      with open(fileadd, 'r') as file:
         yaml_data = yaml.load(file, Loader=yaml.FullLoader)
         id=yaml_data['_id']
         rate=yaml_data['rate']
         agent=yaml_data['agent']
         email=yaml_data['email']
         job_name=yaml_data['job_name']
         state=yaml_data['state']
         description=yaml_data['description']
         cons=yaml_data['cons']
         date=yaml_data['date']
         if not redis_client.get(id):
            #inserting to elastic
            #flag reviwe in redis
            redis_client.set(id, 1)









































