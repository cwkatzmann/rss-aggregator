import sys
import time
import yaml
import argparse
from consumers import RSSConsumer, RSSLinkContentConsumer, ConsoleConsumer
from producers import DiscourseProducer, ElasticsearchProducer, ConsoleProducer


def main(args, conf):
    """
    The entrypoint to the application.
    """
    # load consumer dependencies
    if args.consumer == 'RSSConsumer':
        consumers = [
            RSSConsumer(feed['url'])
            for feed in conf['rss_feeds']
        ]
    elif args.consumer == 'RSSLinkContentConsumer':
        consumers = [
            RSSLinkContentConsumer(feed_addr)
            for feed_addr in conf['rss_feeds']
        ]
    else:
        consumers = [
            ConsoleConsumer()
        ]

    # load producer dependencies
    if args.producer == 'DiscourseProducer':
        producer = DiscourseProducer(conf['discourse_url'], conf['topic_id'], conf['rss_feeds'])
    elif args.producer == 'ElasticsearchProducer':
        producer = ElasticsearchProducer(args.producer_dest, 'rss')
    else:
        producer = ConsoleProducer()

    new_posts = []
    for consumer in consumers:
        new_posts += consumer.get_new_posts()

    print("found {} new posts".format(len(new_posts)))

    for post in new_posts:
        # hard delay so we don't get ratelimited
        time.sleep(3)
        producer.send(post)
        # TODO: save post id for later check

    print("done posting.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI argument parser")
    parser.add_argument('--config-file', dest='path_to_config_file', action='store',
                        help='the relative path to the config file.')

    parser.add_argument('--consumer', dest='consumer', action='store',
                        help='the consumer to be used. options: ConsoleConsumer, RSSConsumer, RSSLinkContentConsumer')
    parser.add_argument('--producer', dest='producer', action='store',
                        help='the producer to be used. options:\
                        ConsoleProducer, ElasticSearchProducer, DiscourseProducer')

    parser.add_argument('--producer-dest', dest='producer_dest', action='store',
                        help='the producer destination url. currently only used by ElasticsearchProducer.')

    args = parser.parse_args(sys.argv[1:])
    next_run_time = 0

    while True:
        now = time.time()
        if now > next_run_time:
            with open(args.path_to_config_file) as configfile:
                conf = yaml.load(configfile)
                main(args, conf)
                next_run_time = now + conf['interval_in_seconds']
        time.sleep(5)
