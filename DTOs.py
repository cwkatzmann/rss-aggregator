import json

class Post:
    def __init__(self, title, content, source_url, _id=None):
        self.title = title
        self.content = content
        self.id = _id
        self.source_url = source_url

    def __str__(self):
        return "title: {}\ncontent: {}".format(self.title, self.content)