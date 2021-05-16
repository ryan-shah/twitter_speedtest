import tweepy
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime

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
graph_image = config['FILES']['graph_image']
yesterday = datetime.date.today() - datetime.timedelta(days=1)

# Connect to twitter
print("connecting to twitter")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Read data from csv
print("Reading CSV")

hours = []
pings = []
downloads = []
uploads = []

with open(csv_file) as file:
	reader = csv.reader(file)
	for row in reader:
		hours.append(row[0])
		pings.append(row[1])
		downloads.append(row[2])
		uploads.append(row[3])

# Wipe old data from csv file
print("Clearing CSV")

file = open(csv_file, 'r+')
file.truncate(0)
file.close()

# Graph data
print("Graphing Data")

plt.plot(hours, downloads, 'bo-', label="Download Speed")
plt.plot(hours, uploads, 'ro-', label="Upload Speed")
plt.xlabel("Hour")
plt.ylabel("Speed - Mbps")
plt.title("Upload/Download Speeds on " + str(yesterday))
plt.legend()
plt.savefig(graph_image)

# Tweet results
print("tweeting results")
status = "Internet usage for " + str(yesterday)
print(status)
api.update_with_media(graph_image, status)
