import subprocess
#########################
#    VARIABLES (both hard drives)
#########################
source_base_dir = "C:\\"
destination_base_dir = "F:\\"
directories = ['bookmarks','gns3','learning','kindle','makeshift\\files','makeshift\\python','music','pictures','programs','text','videos']
#########################
#    2012 small backup
#########################
source_base_dir = "C:\\"
destination_base_dir = "F:\\"
directories = ['bookmarks','gns3','kindle', 'makeshift\\files','makeshift\\python','music','pictures','text','videos\\videos']
#########################
#    XCOPY
#########################
#/y - always allows YES
#/s - is the recursive option
#/i - will make a new directory
#/d - only copy files that do not exist already!!! VERY IMPORTANT
for directory in directories:
	source_dir = source_base_dir + directory
	destination_dir = destination_base_dir + directory	
	print("\n######\n" + directory + "\n######")
	subprocess.call(['xcopy',source_dir,destination_dir,'/y','/s','/i','/d'])