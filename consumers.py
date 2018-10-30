import time
import datetime
import feedparser

from DTOs import Post


class RSSConsumer:
    def __init__(self, url):
        self.url = url

    def get_new_posts(self):
        """collects all new content at self.url"""
        rss = feedparser.parse(self.url)
        posts = []
        
        for item in rss.entries:
            posts.append(Post(item.title, "{}\n{}".format(item.link, item.description)))

        return posts

class ConsoleConsumer:
    def __init__(self, url):
        self.url = url

    def get_new_posts(self):
        """runs in an infinite loop until user breaks out"""
        posts = []

        while True:
        
            try:
                title = input('title: ')
                content = input('content: ')
                posts.append(Post(title, content))
            except KeyboardInterrupt:
                break
        
        return posts