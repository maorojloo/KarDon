from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# create a connection to Elasticsearch
es = Elasticsearch(['localhost:9200'])

# define the index name and documents
index_name = 'my_index'

# Document gets retrived from kafka 



# create a generator function that yields the documents in the correct format
def tajrobe_generator(documents):
    for document in documents:
        yield {
            "_index": index_name,
            "_source": document
        }

def kardon_generator(docmuents):
  for document in documents:
    yield {
          "_index": index_name,
          "_source": document
          }

# use the bulk helper function to insert the documents into Elasticsearch
res = bulk(es, tajrobe_generator(documents), kardon_generator(documents))

# print the response from Elasticsearch
print(res)


