import os
from git import Repo
import shutil
import indexer_v2  
import redis
import yaml

repo_url = 'https://github.com/tajrobe/tajrobe.github.io.git'
current_file_path = str(os.path.dirname(__file__)+'/tajrobe-repo')

# print(current_file_path)

redis_client = redis.Redis(host='localhost', port=6379, password='kardon!!213',  db=2)

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

example_doc={                              
         "_id" : 0,
         "description" :"" ,
         "rate" : 0,
         "agent" :"",
         "email" :"",
         "job_name" :"",
         "state" :"",
         "description" :"", 
         "cons" : "",
         "date" : "",
         "pros" :"",
   }


def dict_remover_empty(dict,key):
    for i in dict:
        if dict[i] == key:
            del dict[i]
        return dict


clone_repository(repo_url, current_file_path)
def deepupdate(original, update):
    """Recursively update a dict.

    Subdict's won't be overwritten but also updated.
    """
    for key, value in original.items():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            deepupdate(value, update[key])
    return update


reviews_path=current_file_path+'/_data/review/'
companys_list = get_folders_in_directory(reviews_path)
docs = []
for company in companys_list:
   company_review_path=reviews_path+company
   files=get_files_in_directory(company_review_path)

   for fileName in files:
      filePath=company_review_path+"/"+fileName
      with open(filePath, 'r') as file:
         yaml_data = yaml.load(file, Loader=yaml.FullLoader)
         yaml_data=deepupdate(example_doc,yaml_data)

         id=yaml_data['_id']
         rate=yaml_data['rate']
         agent=yaml_data['agent']
         email=yaml_data['email']
         job_name=yaml_data['job_name']
         state=yaml_data['state']
         description=yaml_data['description']
         cons=yaml_data['cons']
         date=yaml_data['date']
         pros=yaml_data['pros']
         if not redis_client.get(id):
            #inserting to elastic
            doc={                              
                  "Id" : id,
                  "description" :description ,
                  "rate" : rate,
                #   "agent" :agent,
                  "email" :email,
                  "job_name" :job_name,
                  "job_state" :state,
                  "description" :description, 
                  "cons" : cons,
                  "pros" :pros,
                  "date" : date
            }
            dict_remover_empty(doc,"")
            
            docs.append(doc)
            if len(docs) == 100:
               res= indexer_v2.bulker(docs)
               print(res)
               docs=[]
            #flag reviwe in redis
               redis_client.set(id, 1)









































