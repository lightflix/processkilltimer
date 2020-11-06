#simple script to kill a process after a certain time
#by Calvin Menezes
#progress bar made by Graeme Brodie

from datetime import datetime, timedelta
import os 
import sys
import argparse
import time
import psutil
import threading
import time

#kill signal used
KILL_SIGNAL = 9

#class for color coding printed text ANSI
class bcolors:
    HEADER = '\033[95m'
    DULLBLUE = '\033[94m'
    BRIGHTGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProgressBar:

	PROGRESS_BAR_LENGTH = 40

	CURSOR_HIDE  = "\x9b\x3f\x32\x35\x6C"
	CURSOR_SHOW  = "\x9b\x3f\x32\x35\x68"
	CURSOR_UP    = "\x1b\x5bA"
	CLEAR_LINE   = "\x1b\x5bK"

	PROGRESS_CHARACTER = bcolors.DULLBLUE+"\u2592"+bcolors.ENDC

	# display progress through the file
	def progress_spinner_func(self):
		spinner = [bcolors.DULLBLUE+'|'+bcolors.ENDC, bcolors.DULLBLUE+'/'+bcolors.ENDC, bcolors.DULLBLUE+'-'+bcolors.ENDC, bcolors.DULLBLUE+'\\'+bcolors.ENDC] 
		state = 0
		while not self.done:
			self.progress_bar = (self.currentpoint / self.endpoint) * ProgressBar.PROGRESS_BAR_LENGTH			
			percent_complete  = str(int((self.progress_bar / ProgressBar.PROGRESS_BAR_LENGTH) * 100))
			print("\r\t"+bcolors.DULLBLUE+"["+bcolors.ENDC+ (ProgressBar.PROGRESS_CHARACTER * int(self.progress_bar)) + (" " * (ProgressBar.PROGRESS_BAR_LENGTH - int(self.progress_bar))) +bcolors.DULLBLUE+"] "+bcolors.ENDC + percent_complete + "% " + spinner[state], end="")

			if(self.text is not None):
				print("\n" + ProgressBar.CLEAR_LINE + self.text + "\r" + ProgressBar.CURSOR_UP, end="")
			else:
				print("\n" + ProgressBar.CLEAR_LINE + "\r" + ProgressBar.CURSOR_UP, end="")

			state = (state + 1) % 4
			time.sleep(0.1)		

	def __init__(self, one_hundred_percent_value):
		self.done         = False
		self.endpoint     = one_hundred_percent_value # the value at the end of the bar
		self.currentpoint = 0

		self.progress_bar = 0
		self.text         = None

		if(self.endpoint <= 0):
			raise ValueError("Endpoint for progress bar cannot be <=0")

	def start(self):
		spinner_thread = threading.Thread(target=self.progress_spinner_func)
		spinner_thread.start()
		self.start_time = int(time.time())
		print(ProgressBar.CURSOR_HIDE, end="")

	def finish(self):
		self.done = True
		time_taken = int(time.time() - self.start_time)
		print("\r\t"+bcolors.DULLBLUE+"["+bcolors.ENDC + (ProgressBar.PROGRESS_CHARACTER * ProgressBar.PROGRESS_BAR_LENGTH) +bcolors.DULLBLUE+"] 100% Done"+bcolors.ENDC +" ("+ str(time_taken) + "s)")
		print(ProgressBar.CLEAR_LINE + ProgressBar.CURSOR_SHOW, end="")

	def update_with_text(self, new_value, text):
		self.currentpoint = new_value
		self.text         = text

	def update(self, new_value):
		self.update_with_text(new_value, None)		

	def increment(self, increment_value):
		self.update(self.currentpoint + increment_value)

#function that calculates time at which process gets killed
def kill_timestamp(no_of_seconds):
	current_time = datetime.now()
	new_time = current_time + timedelta(seconds = no_of_seconds)
	print("\tETA {}:{}:{}, {}/{}/{}".format(new_time.hour, new_time.minute, new_time.second, new_time.day, new_time.month, new_time.year))

#timer function, takes in seconds parameter
def timer(sec):

	pbar = ProgressBar(sec)

	print(bcolors.DULLBLUE+"\n\tTimer started\n"+bcolors.ENDC)

	#call function to calculate new time
	kill_timestamp(sec)

	pbar.start()

	for i in range(0, sec+1):
		pbar.update(i)
		time.sleep(1)

	pbar.finish()


	print(bcolors.DULLBLUE+"\n\tTimer ended\n"+bcolors.ENDC)
	return


# #timer function, takes in seconds parameter
# def timer(sec):
# 	print(bcolors.DULLBLUE+"\n\tTimer started"+bcolors.ENDC)

# 	#call function to calculate new time
# 	kill_timestamp(sec)

# 	#start timer
# 	time.sleep(sec)

# 	print(bcolors.DULLBLUE+"\tTimer ended\n"+bcolors.ENDC)
# 	return

#process kill function, takes in PID parameter.
def killer(pid):

	try:
		#kills process with given signal
		os.system("kill -"+str(KILL_SIGNAL)+" "+str(pid))
	except:
		print(bcolors.FAIL+"Error: PID "+str(pid)+" does not exist or it might have changed. Exiting...\n"+bcolors.ENDC)
	else:
		print(bcolors.BRIGHTGREEN+"Process killed. Exiting...\n"+bcolors.ENDC)
	exit()

#function to find process name from PID
def process_finder(pid):

	try:
		#using psutil module to fetch process information
		process = psutil.Process(pid)
		process_name = process.name()
	except:
		print(bcolors.FAIL+"Error: PID "+str(pid)+" does not exist. Exiting...\n"+bcolors.ENDC)
		exit()
	else:
		return process_name

#main function
def main():

	parser = argparse.ArgumentParser()

	#two command-line arguments, PID and TIME in seconds.
	parser.add_argument("pid", help="PID of process",type=int)
	parser.add_argument("time", help="Process kill countdown time in seconds",type=int)
	args = parser.parse_args()


	print(bcolors.HEADER+"\n\t---==== PROCESS KILLER ====---\n"+bcolors.ENDC)

	#get process name
	process_name = process_finder(args.pid)

	#defining answer variable
	answer = "null"

	#keep looping until answer is valid
	while(answer.lower() != "y" and answer.lower() != "n"):
		answer = input("Do you want to kill "+bcolors.BRIGHTGREEN+bcolors.BOLD+process_name+bcolors.ENDC+" in "+str(args.time)+" seconds? (Y/N): ")

	if(answer == 'y'):
		#if answer is y, start timer and call killer
		timer(args.time)
		killer(args.pid)
	else:
		#if answer is n, do nothing and exit
		print("Exiting...\n")
		exit()

if __name__ == "__main__":
    main()