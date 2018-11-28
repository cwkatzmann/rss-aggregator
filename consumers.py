import time
import json
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

class RSSLinkContentConsumer:
    def __init__(self, url):
        self.url = url
    
    def get_new_posts(self):
        """collects all content at self.url, checks if that content has been seen,
        follows content links if not seen yet, returns list of documents found by following links
        with ther RSS IDs."""
        rss = feedparser.parse(self.url)
        posts = []

        for item in rss.entries:
            response = requests.get(item.link)
            
            if 200 <= response.status_code <= 299:
                body = {
                    text: response.text,
                    _id: item.id
                }
                
                posts.append(Post(item.title, body, item.id))
        
        return posts


    def seen_before(_id):
        """checks if a post with that id has been seen before."""
        pass


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