from datetime import datetime
import time 
from elasticsearch_dsl import (Document, Date, Integer,Keyword, Text , Long ,InnerDoc, Float, Boolean,Object, Short , Byte)
from elasticsearch_dsl.connections import connections

ELASTIC_HOSTS_CONFIG = ['elastic:KardonCoolPass1x3@localhost:9208']
connections.create_connection(hosts=ELASTIC_HOSTS_CONFIG)

ALIAS = 'kardon1'
PATTERN = ALIAS + '-*'

PERSIAN_ANALYZER = 'persian_grams_index_analyzer'
PERSIAN_SEARCH_ANALYZER = 'persian_grams_search_analyzer'

class NormalDoc(InnerDoc):
    titleFa = Text(analyzer=PERSIAN_ANALYZER, search_analyzer=PERSIAN_SEARCH_ANALYZER)
    titleEn = Text()

class Review(Document):
    Id = Long()
    description = Object(NormalDoc)
    rate = Text()
    agent = Text()
    email = Keyword()
    job_name = Text()
    state = Text()
    description = Text()
    cons = Keyword(multi=True)
    date = Text()

