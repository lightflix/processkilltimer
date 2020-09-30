#simple script to kill a process after a certain time
#made by Calvin Menezes

import os 
import sys
import argparse
import time
import psutil

#kill signal used
KILL_SIGNAL = 2

#class for color coding printed text ANSI
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#timer function, takes in seconds parameter
def timer(sec):
	print(bcolors.OKBLUE+"\n\tTimer started"+bcolors.ENDC)

	#start timer
	time.sleep(sec)

	print(bcolors.OKBLUE+"\tTimer ended\n"+bcolors.ENDC)
	return

#process kill function, takes in PID parameter.
def killer(pid):

	try:
		#kills process with given signal
		os.system("kill -"+str(KILL_SIGNAL)+" "+str(pid))
	except:
		print(bcolors.FAIL+"Error: PID "+str(pid)+" does not exist or it might have changed. Exiting...\n"+bcolors.ENDC)
	else:
		print(bcolors.OKGREEN+"Process killed. Exiting...\n"+bcolors.ENDC)
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
		answer = input("Do you want to kill "+bcolors.OKGREEN+bcolors.BOLD+process_name+bcolors.ENDC+" in "+str(args.time)+" seconds? (Y/N): ")

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