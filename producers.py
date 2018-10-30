import requests
import json


class ConsoleProducer:
    def __init__(self, category):
        self.category = category
    
    def send(self, post):
        print("category: " + self.category + "\npost: " + str(post))

class DiscourseProducer:
    def __init__(self, url, category):
        self.category = category
        self.url = url
    
    def send(self, post):
        data = {"title": post.title, "raw": post.content, "category": self.category}
        res = requests.post(self.url, headers={'content-type': 'application/json'}, data=json.dumps(data))
        print("sent post: {} got status: {}".format(post, res.status_code))