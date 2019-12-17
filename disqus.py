import urllib.request
import json
import string
import sys

#disqus variables & dialog
secret_key = ''
public_key = ''
print()
print('')
print()
#4636285904
forum = input("Insert name of forum: ")
thread = input("Insert thread ID: ")
number_of_comments = int(input("Insert number of comments: "))
limit = 100
api_calls = int(number_of_comments / limit)
#other variables
destination_file = 'C:/scripts/disqus.txt'
post_list = []
cursor = False
counter_inside_response_loop = 0 #only purpose is to show user output with modulus 10
#loop and make multiple api calls
for api_call_count in range(api_calls):
	
	#example of python string interpolation
	endpoint = 'https://disqus.com/api/3.0/threads/listPosts.json?api_key={public_key}&thread={thread}&forum={forum}&limit={limit}'.format(**locals())
	#This Python version of a ternery operator is responsible for cursors, going into the next page so to speak
	#If condition is in the middle, unlike in PHP
	endpoint = endpoint + "&cursor=" + cursor if cursor else endpoint
	#this is how web page or api requests are read in python
	#when this is done, this is a string with json.l If you don't decode, than it's python bytes object. HTTP always returns RAW bytes
	#Each API call returns 100 posts, verified by len(disqus_response_dictionary)
	#The reason for cp1252 is because of import sys, print(sys.stdout.encoding) for sublime text editor
	disqus_response = urllib.request.urlopen(endpoint).read().decode('cp1252')
	#this is the equivalent of json_decode(json,TRUE) in PHP. It turns a string of JSON into a dictionary (or array as I know it)
	disqus_response_dictionary = json.loads(disqus_response)
	#This will get the cursor. Other variables are in the for loop
	cursor = disqus_response_dictionary['cursor']['next']
	#iterate through response
	for response_node in disqus_response_dictionary['response']:
		try:
			#variables inside loop
			username = response_node['author']['username'] if response_node['author']['username'] else "???"
			likes = response_node['likes']
			dislikes = response_node['dislikes']
			comment = response_node['raw_message'].strip()
			#alternative way to remove non-ascii characters from list
			comment = ''.join([x for x in comment if ord(x) < 128])
			date = response_node['createdAt']
			#put in another array, or dictionary
			#print(comment)
			stripped_data_dict = {'username': username, 'comment':comment,'likes': likes, 'dislikes': dislikes, "date" : date}
			post_list.append(stripped_data_dict)
			#PRINTING let us know progress as it goes
			counter_inside_response_loop += 1
			if counter_inside_response_loop % 10 == 0:
				print(counter_inside_response_loop)
				print(comment)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			continue


#sorting by two criteria
post_list.sort(key=lambda node: (node['likes'], node['dislikes']))
#open file
f = open(destination_file,'a')
#iterate through the stripped down version, made separate to do the sort
for post_list_node in post_list:
	#make text to put in file
	text = '---' + str(post_list_node['likes']) + ',' + str(post_list_node['dislikes']) + '-----' + post_list_node['username'] + '\n'
	text += post_list_node['comment'] + '\n'
	f.write(text)
#close file, and actually put this stuff in the file when closing
f.close()

