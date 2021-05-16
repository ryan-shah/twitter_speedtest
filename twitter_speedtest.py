import speedtest
import tweepy
import csv
import datetime
import configparser

# Open config file
print("reading config file")
config = configparser.ConfigParser()
config.read('config.ini')

# Pull data from config file
consumer_key = config['TWITTER']['consumer_key']
consumer_secret = config['TWITTER']['consumer_secret']
access_token = config['TWITTER']['access_token']
access_token_secret = config['TWITTER']['access_token_secret']
csv_file = config['FILES']['csv_file']
hour = datetime.datetime.now().hour

# Connect to twitter
print("connecting to twitter")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Do speedtest
speed_test = speedtest.Speedtest()
speed_test.get_best_server()

print("getting ping")
ping = speed_test.results.ping

print("getting download")
download = speed_test.download()

print("getting upload")
upload = speed_test.upload()

download_mbs = round(download / (10**6), 2)
upload_mbs = round(upload / (10**6), 2)

# Create Status
status = "Ping: " + str(ping) + " ms\n"
status += "Download: " + str(download_mbs) + " Mbps\n"
status += "Upload: " + str(upload_mbs) + " Mbps\n"
status += "Expected Download: 100 Mbps\n"
status += "Difference: " + str(100.0 - download_mbs) + " Mbps"
print(status)

# Tweet Result
print("tweeting results")
#api.update_status(status)

# Write data to CSV
print("writing data to "+csv_file)

data = [hour, ping, download_mbs, upload_mbs]

with open(csv_file, 'a') as file:
	writer = csv.writer(file)
	writer.writerow(data)
