# twitter_speedtest
```
python twitter_speedtest.py -h
usage: twitter_speedtest.py [-g] [-i <inputfile>]
        -g: graph mode - read from csv and generate graph of past data
                NOTE: Will empty csv after run
        -i <inputfile>: will use inputfile as config. Defaults to config.ini.
```

A group of scripts to make monitoring network speeds more convenient.

There are two main functions:
- Tweet current network status

`python twitter_speedtest.py`

- Tweet graph of past network usage

`python twitter_speedtest.py -g`

## view in action
[![Twitter URL](https://img.shields.io/twitter/follow/RyansWifiSpeed)](https://twitter.com/RyansWifiSpeed)

Run via crontab
```
4 * * * * /usr/bin/python ~/twitter_speedtest/twitter_speedtest.py > speedtest_log.txt 2>&1
0 0 * * * /usr/bin/python ~/twitter_speedtest.py -g > speedtest_graph_log.txt 2>&1
```


## configuration
The scripts look for a config.ini file in the current working directory
- custom .ini files can be passed with the `-i` or `--input` argument

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


