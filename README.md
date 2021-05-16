# twitter_speedtest
A group of scripts to make monitoring network speeds more convenient.

There are two main functions:
- Tweet current network status

`python twitter_speedtest.py`

- Tweet graph of past network usage

`python twitter_speedtest_graph.py`

## configuration
The scripts look for a config.ini file in the current working directory

Format should be

```
[TWITTER]
consumer_key=YOUR_CONSUMER_KEY_HERE
consumer_secret=YOUR_CONSUMER_SECRET_HERE
access_token=YOUR_ACCESS_TOKEN_HERE
access_token_secret=YOUR_ACCESS_TOKEN_SECRET_HERE

[FILES]
csv_file=speedtest.csv
graph_image=graph.png
```
## dependencies
- [speedtest-cli](https://github.com/sivel/speedtest-cli)
- [matplotlib](https://matplotlib.org/)
- [tweepy](https://www.tweepy.org/)
