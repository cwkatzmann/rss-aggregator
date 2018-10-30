import json

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return "title: {}\ncontent: {}".format(self.title, self.content)

    def json(self):
        return json.dumps({'title': self.title, 'raw': self.content, 'category': self.category})