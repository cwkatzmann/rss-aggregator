import requests
import json

from elasticsearch import Elasticsearch

class ConsoleProducer:
    def send(self, post):
        print("post: " + str(post))

class DiscourseProducer:
    def __init__(self, url, category, feeds):
        self.category = category
        self.url = url
        self.feeds = feeds

    def send(self, post):
        username = ''
        api_key = ''
        for feed in self.feeds:
            if feed["url"] == post.source_url:
                username = feed["username"]
                api_key = feed["api_key"]

        if not api_key or not username:
            print("could not locate api key or username for url: " + post.source_url)
            pass

        res = requests.post("{}?api_key={}&api_username={}".format(self.url, api_key, username),
                            headers={'content-type': 'application/json'},
                            data=post.json())

        print("sent post: {} got status: {}".format(post, res.status_code))

class ElasticsearchProducer:
    def __init__(self, url, index):
        self.url = url
        self.index = index
        self.client = Elasticsearch()
    
    def send(self, post):
        self.client.index(index=self.index, doc_type="json", id=post.id, body=post.json())