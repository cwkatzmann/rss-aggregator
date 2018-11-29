import requests
import json

from elasticsearch import Elasticsearch

class ConsoleProducer:
    def send(self, post):
        print("post: " + str(post))

class DiscourseProducer:
    def __init__(self, url, category):
        self.category = category
        self.url = url
    
    def send(self, post):
        res = requests.post(self.url, headers={'content-type': 'application/json'}, body=post.json())
        print("sent post: {} got status: {}".format(post, res.status_code))

class ElasticsearchProducer:
    def __init__(self, url, index):
        self.url = url
        self.index = index
        self.client = Elasticsearch()
    
    def send(self, post):
        self.client.index(index=self.index, doc_type="json", id=post.id, body=post.json())