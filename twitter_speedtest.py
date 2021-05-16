import configparser
import csv
import datetime
import getopt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import speedtest
import sys
import tweepy

def readConfig(config_file):
	# Open config file
	print('reading config file: '+config_file)
	config = configparser.ConfigParser()
	config.read(config_file)
	return config

def connectTwitter(config):
	# Pull data from config file
	print('connecting to twitter')
	consumer_key = config['TWITTER']['consumer_key']
	consumer_secret = config['TWITTER']['consumer_secret']
	access_token = config['TWITTER']['access_token']
	access_token_secret = config['TWITTER']['access_token_secret']

	# Connect to twitter
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api

def runSpeedtest():
	# Do speedtest
	speed_test = speedtest.Speedtest()
	speed_test.get_best_server()

	print('getting ping')
	ping = speed_test.results.ping

	print('getting download')
	download = speed_test.download()

	print('getting upload')
	upload = speed_test.upload()

	download_mbs = round(download / (10**6), 2)
	upload_mbs = round(upload / (10**6), 2)

	hour = datetime.datetime.now().hour
	data = [hour, ping, download_mbs, upload_mbs]
	return data

def generateStatus(data, expected):
	# Create Status
	status = 'Ping: ' + str(data[1]) + ' ms\n'
	status += 'Download: ' + str(data[2]) + ' Mbps\n'
	status += 'Upload: ' + str(data[3]) + ' Mbps\n'
	status += 'Expected Download: ' + str(expected) + ' Mbps\n'
	status += 'Difference: ' + str(expected - data[2]) + ' Mbps'
	print(status)
	return status

def tweetStatus(api, status):
	# Tweet Result
	print('tweeting results')
	api.update_status(status)

def writeToCsv(csv_file, data):
	# Write data to CSV
	print('writing data to '+csv_file)

	with open(csv_file, 'a') as file:
		writer = csv.writer(file)
		writer.writerow(data)

def readFromCsv(csv_file):
	data = {
		'hours':[],
		'pings':[],
		'downloads':[],
		'uploads':[]
	}

	# Read data from csv
	print('Reading CSV')
	with open(csv_file) as file:
		reader = csv.reader(file)
		for row in reader:
			data['hours'].append(row[0])
			data['pings'].append(row[1])
			data['downloads'].append(row[2])
			data['uploads'].append(row[3])
	return data

def wipeCsv(csv_file):
	# Wipe old data from csv file
	print('Clearing CSV')
	file = open(csv_file, 'r+')
	file.truncate(0)
	file.close()

def graphData(data, graph_image):
	# Graph data
	print('Graphing Data')
	yesterday = datetime.date.today() - datetime.timedelta(days=1)

	plt.plot(data['hours'], data['downloads'], 'bo-', label='Download Speed')
	plt.plot(data['hours'], data['uploads'], 'ro-', label='Upload Speed')
	plt.xlabel('Hour')
	plt.ylabel('Speed - Mbps')
	plt.title('Upload/Download Speeds on ' + str(yesterday))
	plt.legend()
	plt.savefig(graph_image)

def tweetGraph(api, graph_image):
	# Tweet results
	print('tweeting results')
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	status = 'Internet usage for ' + str(yesterday)
	print(status)
	api.update_with_media(graph_image, status)

def printUsage():
	print('usage: twitter_speedtest.py [-g] [-i <inputfile>]')
	print('\t-g: graph mode - read from csv and generate graph of past data')
	print('\t\tNOTE: Will empty csv after run')
	print('\t-i <inputfile>: will use inputfile as config. Defaults to config.ini.')


def main(argv):
	config_file = 'config.ini'
	graph_mode = False
	try:
		opts, args = getopt.getopt(argv,'ghi:',['input='])
	except getopt.GetoptError:
		printUsage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printUsage()
			sys.exit()
		elif opt == '-g':
			graph_mode = True
		elif opt in ('-i', '--input'):
			config_file = arg

	config = readConfig(config_file)
	csv_file = config['FILES']['csv_file']
	graph_image = config['FILES']['graph_image']
	expected_download = int(config['NETWORK']['expected_download'])

	api = connectTwitter(config)

	if not graph_mode:
		data = runSpeedtest()
		status = generateStatus(data, expected_download)
		tweetStatus(api, status)
		writeToCsv(csv_file, data)
	else:
		data = readFromCsv(csv_file)
		graphData(data, graph_image)
		tweetGraph(api, graph_image)
		wipeCsv(csv_file)

if __name__ == '__main__':
	main(sys.argv[1:])
