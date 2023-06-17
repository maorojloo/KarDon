from datetime import datetime
import time 
from elasticsearch_dsl import (
                              Document, Date, Integer,
                              Keyword, Text , Long ,
                              InnerDoc, Float, Boolean,
                              Object, Short , Byte
                              )
from elasticsearch_dsl.connections import connections

ELASTIC_HOSTS_CONFIG = ['elastic:KardonCoolPass1x3@localhost:9208']
connections.create_connection(hosts=ELASTIC_HOSTS_CONFIG)


ALIAS = 'kardon'
PATTERN = ALIAS + '-*'


PERSIAN_ANALYZER = 'persian_grams_index_analyzer'
PERSIAN_SEARCH_ANALYZER = 'persian_grams_search_analyzer'

class NormalDoc(InnerDoc):
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()
    
class Company(Document):
    Id = Long
    description = Object(NormalDoc)
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()
    company_logo = Keyword()
    hasPicture = Boolean(default=False)
    url = Keyword()
    job_posts = Keyword()
    job_post_count = Short()

class CompanyInfo(InnerDoc):
    name_fa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    name_en = Text()
    about = Object(NormalDoc)
    

class Province(InnerDoc):
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()


class City(InnerDoc):
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class Country(InnerDoc):
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class Location(InnerDoc):
    country = Object(Country)
    province = Object(Province)
    city = Object(City)


class WorkTypes(InnerDoc):
    Id = Integer()
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class JobBoard(InnerDoc):
    organizationColor = Keyword()
    Id = Integer()
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class ActivationTime(InnerDoc):
    passedDays = Short()
    beautifyFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    beautifyEn = Text()
    # Double Check time 
    date = Date()

class AcademicRequirements(InnerDoc):
    Id = Integer()
    levelTitle = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class RequiredEducations(InnerDoc):
    Id = Short()
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class ExpireTime(InnerDoc):
    date = Date()
    days_left_until = Short()

class JobPost(Document):
    title = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    Id = Long()
    url = Keyword()
    description = Text()
    description_clean = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    is_persian = Boolean()
    is_expired = Boolean()
    company_info = Object(CompanyInfo) 
    sourceId = Keyword()
    location = Object(Location)
    work_types = Object(WorkTypes)
    salary = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    gender = Text()
    tags = Text()
    job_board = Object(JobBoard)
    activation_time = Object(ActivationTime)
    normalize_salary_min = Long()
    normalize_salary_max = Long()
    requiredLanguageSkills = Text()
    skills = Keyword()
    required_work_experience = Text()
    has_no_work_experience_requirement = Boolean()
    requiredEducations = Object(RequiredEducations)
    military_service_state = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    is_internship = Boolean()
    has_alternative_military = Boolean()
    is_remote = Boolean()
    hasInsurance = Keyword()
    paymentMethod = Keyword()
    workHours = Keyword()
    seniorityLevel = Keyword()
    benefits = Text()
    requiredKnowledge = Text()
    businessTripsDescription = Text()
    minAge = Byte()
    maxAge = Byte()
    softwareSkills = Text()
    labels = Text()
    publishTime = Object(ActivationTime)
    contactInfo = Text()
    jobPostCategories = Text()
    
    class Index:
        # we will use an alias instead of the index, script_id=elastic_id
        name = ALIAS
        settings = {
            'number_of_shards': 8,
            'number_of_replicas': 1,
            "analysis": {
                "char_filter": {
                    "zero_width_spaces": {
                        "type": "mapping",
                        "mappings": ["\\u200C=> "]
                    }
                },
                "analyzer": {
                    PERSIAN_ANALYZER: {
                        "filter": [
                            "lowercase",
                            "arabic_normalization",
                            "persian_normalization",
                            "persian_grams"
                        ],
                        "char_filter": ["zero_width_spaces"],
                        "tokenizer": "standard"
                    },
                    PERSIAN_SEARCH_ANALYZER: {
                        "filter": [
                            "lowercase",
                            "arabic_normalization",
                            "persian_normalization",
                            "persian_grams_query"
                        ],
                        "char_filter": ["zero_width_spaces"],
                        "tokenizer": "standard"
                    }
                },
                "filter": {
                    "persian_grams": {
                        "type": "common_grams",
                        "stopwords": "_persian_",
                        "common_words": "_persian_"
                    },
                    "persian_grams_query": {
                        "type": "common_grams",
                        "query_mode": "true",
                        "stopwords": "_persian_",
                        "common_words": "_persian_"
                    }
                }
            }
        }

    def save(self, **kwargs):
        self.created_at = datetime.now()
        self.created_timestamp = int(time.time() * 1000)
        return super().save(**kwargs)

# create the mappings in Elasticsearch
#JobPost.init()
