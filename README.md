# mha_postservice
A lightweight service for posting data from an RSS feed to configuration-driven destinations, written in Python.

### Suported Consumer Types:
`RSSConsumer` - consumes the title, link, and description of RSS feed items.
`RSSLinkContentConsumer` - follows the RSS feed items' links and consumes their title and the content returned by a request to the link urls.
`ConsoleConsumer` - for development and manual testing. Prompts the user for input via stdin.

### Supported Producer Types:
`ElasticsearchProducer` - produces data to Elasticsearch.
`DiscourseProducer` - produces data to [Discourse](https://www.discourse.org/) in the form of a message board post.
`ConsoleProducer` - for development and manual testing. Produces data to stdout.

### Deploy:
Included is a systemd .service file and an example config.yaml file.
You will need to modify these files for your specifc needs.

1) Run the init.py script to set up the sqlite3 db which keeps track of which RSS items have been posted.
1) Alter the User and ExecStart fields in the systemd service file to work with your environment in the service file.
1) Provide a list of the urls for the RSS feeds you wish to aggregate in the config file.
1) (optional) If you are using the Discourse producer, provide the url with api key for your Discourse instance in the config file.
1) Choose the consumer you would like to use from the options specified above.
1) Choose the producer from the options specified aboce.

### Example run commands:
Producing RSS link content to Elasticsearch:
`python main.py --config-file ./config.yaml --consumer=RSSLinkContentConsumer --producer=ElasticsearchProducer --producer-dest=localhost:9200`

Producing RSS titles, links, descriptions to Discourse:
`python main.py --config-file ./config.yaml --consumer=RSSConsumer --producer=DiscourseProducer`

Producing user-prompted stdin to stdout (KeyboardInterrupt to stop consumer)
`python main.py --config-file ./config.yaml --consumer=ConsoleConsumer --producer=ConsoleProducer`
