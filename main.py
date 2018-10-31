import sys
import time
import yaml
import argparse
from consumers import RSSConsumer
from producers import DiscourseProducer


def main(conf):
    consumers = [
        RSSConsumer(feed_addr)
        for feed_addr in conf['rss_feeds']
    ]
    producer = DiscourseProducer(conf['discourse_url'], conf['topic_id'])

    new_posts = []
    for consumer in consumers:
        new_posts += consumer.get_new_posts()

    print("found {} new posts".format(len(new_posts)))

    for post in new_posts:
        time.sleep(3)
        producer.send(post)

    print("done posting.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI argument parser")
    parser.add_argument('--config-file', dest='path_to_config_file', action='store', help='the relative path to the config file.')
    args = parser.parse_args(sys.argv[1:])
    
    next_run_time = 0

    while True:
        now = time.time()
        if now > next_run_time:
            with open(args.path_to_config_file) as configfile:
                conf = yaml.load(configfile)
                main(conf)
                next_run_time = now + conf['interval_in_seconds']
        
        time.sleep(5)
        