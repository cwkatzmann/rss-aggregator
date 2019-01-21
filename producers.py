import requests
import json

from elasticsearch import Elasticsearch

class ConsoleProducer:
    def send(self, post):
        print("post: " + str(post))

class DiscourseProducer:
    def __init__(self, url, category, sources):
        self.url = url
        self.category = category
        self.sources = sources

    def send(self, post):
        username = ''
        api_key = ''
        for source in self.sources:
            for url in source['urls']:
                if url == post.source_url:
                    username = source['username']
                    api_key = source['api_key']

        if not api_key or not username:
            print("could not locate api key or username for url: " + post.source_url)
            pass

        res = requests.post("{}?api_key={}&api_username={}".format(self.url, api_key, username),
                            headers={'content-type': 'application/json'},
                            data=json.dumps(
                                {
                                    "title": post.title,
                                    "raw": post.content,
                                    "category": self.category
                                }
                                )
                            )

        print("sent post: {} got status: {}".format(post, res.status_code))

class ElasticsearchProducer:
    def __init__(self, url, index):
        self.url = url
        self.index = index
        self.client = Elasticsearch()
    
    def send(self, post):
        self.client.index(index=self.index, doc_type="json", id=post.id, body=post.content)