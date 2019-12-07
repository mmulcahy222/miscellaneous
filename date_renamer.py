#########################
#    IMPORTS
#########################
import ctypes 
import ctypes.wintypes as wt
from os import listdir

#########################
#    variable
#########################
GENERIC_READ = 2147483648 
GENERIC_WRITE = 1073741824 
FILE_SHARE_READ = 1 
FILE_SHARE_WRITE = 2
CREATE_ALWAYS = 2
OPEN_EXISTING = 3 
base_folder = "C:/Videos/TabletVideos/old/"

#########################
#    functions
#########################
#leading zeroes
def lz(val):
	return "{0:0>2}".format(val)
def sanitize(word):
	return str(''.join([x for x in str(word) if ord(x) < 128]))
#SYSTEMTIME C Struct
class SYSTEMTIME(ctypes.Structure):
	_fields_=[('wYear',wt.WORD), ('wMonth',wt.WORD), ('wDayOfWeek',wt.WORD), ('wDay',wt.WORD), ('wHour',wt.WORD), ('wMinute',wt.WORD), ('wSecond',wt.WORD), ('wMilliseconds',wt.WORD)]

#########################
#    code
#########################

def get_modified_date(filename):
	#
	# File Open in Windows
	#
	# https://docs.microsoft.com/en-us/windows/desktop/api/fileapi/nf-fileapi-createfilea
	CreateFileA = ctypes.windll.kernel32.CreateFileA
	file_handle = wt.HANDLE(CreateFileA(filename.encode(),0x80000000, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None ))
	# print("FILE HANDLE",file_handle)
	# print("GET LAST ERROR",ctypes.GetLastError())
	#
	# GET TIME
	#
	# https://msdn.microsoft.com/en-us/9baf8a0e-59e3-4fbd-9616-2ec9161520d1
	#this is how to make a pointer. This is then <ctypes.wintypes.LP_FILETIME> object
	#I wish I knew what (ctypes.c_int*30)(100) meant. See if that can be figured out
	#it makes a pointer to be filled up by a windows API call (GetFileTime)
	file_time_struct_pointer = ctypes.cast((ctypes.c_int*1)(1), ctypes.POINTER(wt.FILETIME))
	GetFileTime = ctypes.windll.kernel32.GetFileTime
	#restype is the value that's returned
	# GetFileTime.restype = wt.BOOL
	#argtypes removes need to encapsulate arguments with Windows data types
	# GetFileTime.argtypes = [wt.HANDLE,wt.LPFILETIME]
	#restype & argtypes are both generally called to shorten the syntax
	#file_time_struct_pointer just gets filled up with correct values
	GetFileTime(file_handle,0,0,file_time_struct_pointer)
	# print("FILE STRUCT POINTER", file_time_struct_pointer.contents.dwLowDateTime)
	# print("GET LAST ERROR",ctypes.GetLastError())
	# 
	# CONVERT FILE STRUCT TO NORMAL TIME
	#
	# https://msdn.microsoft.com/en-us/library/windows/desktop/ms724280(v=vs.85).aspx
	system_time_struct_pointer = ctypes.cast((ctypes.c_int*1)(1), ctypes.POINTER(SYSTEMTIME))
	FileTimeToSystemTime = ctypes.windll.kernel32.FileTimeToSystemTime
	#No argstype or restype needed
	FileTimeToSystemTime(file_time_struct_pointer,system_time_struct_pointer)
	# print(system_time_strugct_pointer.contents.wYear)
	# print("GET LAST ERROR",ctypes.GetLastError())
	#Get Date_Time_Contents
	system_time_contents = system_time_struct_pointer.contents
	year = str(system_time_contents.wYear)
	month = str(system_time_contents.wMonth)
	day_of_week = str(system_time_contents.wDayOfWeek)
	day = str(system_time_contents.wDay)
	hour = str(system_time_contents.wHour)
	minute = str(system_time_contents.wMinute)
	second = str(system_time_contents.wSecond)
	milliseconds = str(system_time_contents.wMilliseconds)
	modified_date_string = lz(year) + lz(month) + lz(day) + '_' + lz(hour) + lz(minute) + lz(second)
	#CLOSE HANDLE
	#
	#Necessary for renaming and for preventing "Used By Another Program Errors"
	CloseHandle = ctypes.windll.kernel32.CloseHandle
	CloseHandle(file_handle)
	return modified_date_string


def rename_file(old_filename,new_filename):
	mfa = ctypes.windll.kernel32.MoveFileA
	old_filename = old_filename.encode()
	new_filename = new_filename.encode()
	return mfa(old_filename,new_filename)

if __name__ == "__main__":
	all_file_names = [sanitize(file) for file in listdir(base_folder)]
	for file_name in all_file_names:
		 full_source_file_name = base_folder + file_name
		 modified_date_windows = get_modified_date(full_source_file_name)
		 full_dest_file_name = base_folder + modified_date_windows + "___" + file_name
		 print("<<<<  %s  >>> has changed to <<<  %s  >>>" % (full_source_file_name,full_dest_file_name))
		 rename_file_result = rename_file(full_source_file_name,full_dest_file_name)
		 print("%s" % rename_file_result)
		 print("\n")
		 error = ctypes.GetLastError()
		 if error != 0:
		 	print("ERROR: ",error)
		 	print("\n")




		
