import os
import re
import sys
from helpers import *
from PIL import Image

#########################
#
#    TO RUN THIS, USE EITHER COMMAND LINE OR PUT DIRECTORY BELOW:
#    EXAMPLE: image_reduce.py flickr_2017 flickr_2019
#
#########################

media_directory = 'C:/images/'
#default directory path
source_last_levels = ['images22/']
#if command line arguments, give different source
if len(sys.argv) > 1:
	source_last_levels = sys.argv
	source_last_levels.pop(0)
	#This regex ensures that there will always be one slash at the end, whether the user entered no slashes, or multiple
	source_last_levels = list(map(lambda x: re.sub('\/*$','/',x),source_last_levels))



#100000 = 100 KB
#I realize I could have put this into classes. But I wanted this done fast. 
flickr_quality_directory = {0: 80,
	 100000: 75,
	 200000: 75,
	 300000: 70,
	 400000: 65,
	 500000: 40,
	 600000: 25,
	 700000: 22,
	 800000: 18,
	 900000: 13}
pictures_quality_directory = {0: 80,
	 100000: 65,
	 200000: 50,
	 300000: 40,
	 400000: 40,
	 500000: 30,
	 600000: 25,
	 700000: 22,
	 800000: 18,
	 900000: 13}
bytes_quality_directory = flickr_quality_directory
def get_quality(bytes_picture):
	#BREAK if the next key is larger
	for bytes_threshold,quality in bytes_quality_directory.items():
		if(bytes_picture < bytes_threshold):
			break
		past_quality = quality
	return past_quality

def copy_compressed_image(original_full_path, destination_full_path, quality):
	try:
		image = Image.open(original_full_path)
	except OSError:
		print(f"{original_full_path} COULD NOT OPEN")
		file_add_contents("logs.txt",f"{original_full_path} COULD NOT OPEN\n")
		return
	destination_full_path = destination_full_path
	if destination_full_path.endswith('png'):
		image = image.convert("RGB")
		destination_full_path = destination_full_path.replace("png","jpg")
		#don't need to lower quality because png to jpg is enough
		quality = 70
	try:
		image.save(destination_full_path,quality=quality)
		print(f"{count}> (ORIGINAL BYTES = {file_bytes}) Copying from {source_full_path} to {destination_full_path}")
	except:
		print(f"{destination_full_path} DID NOT SAVE")
		file_add_contents("logs.txt",f"{original_full_path} DIDN'T SAVE\n")
		return
		

#TESTING
if __name__ == '__main__':
	for source_last_directory_name in source_last_levels:
		count = 0
		start = 0
		end = 3000000
		#add _n to destination
		destination_last_directory_name = re.sub('(\/)',r'_r\1',source_last_directory_name)
		source_directory = media_directory + source_last_directory_name
		destination_directory = media_directory + destination_last_directory_name
		print('\n\n\n\n\n')
		if os.path.exists(destination_directory) is False:
			try:
				os.mkdir(destination_directory)
				print(f"CREATED {destination_directory}")
			except FileExistsError: 
				print("DIRECTORY ALREADY EXISTS")
		print(f"####YOU'RE IN {source_directory}, COPYING IN {destination_directory}")
		try:
			for root, dirs, files in os.walk(source_directory):
				for name in files:
					if '.jpg' in name or '.png' in name or '.gif' in name:
						source_full_path = source_directory + name
						destination_full_path = destination_directory + name
						try:
							file_bytes = os.stat(source_full_path).st_size
						except:
							file_bytes = 100
						quality = get_quality(file_bytes)
						count += 1
						destination_full_path = re.sub('(\.jpg|\.png|\.gif)',"_" + str(quality) + r"\1",destination_full_path)
						if count < start:
							continue
						if count == end:
							raise StopIteration
						copy_compressed_image(source_full_path,destination_full_path,quality)
								
		except StopIteration:
			print("Finished running through loop")

