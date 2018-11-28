import json

class Post:
    def __init__(self, title, content, _id=None):
        self.title = title
        self.content = content
        self.id = _id

    def __str__(self):
        return "title: {}\ncontent: {}".format(self.title, self.content)

    def json(self):
        data = {
            'title': self.title,
            'raw': self.content,
            }

        if self.id :
            data['id'] = self.id
        
        return json.dumps(data)