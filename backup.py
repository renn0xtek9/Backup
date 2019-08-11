#!/usr/bin/env python3
import datetime
import codecs
import getpass
import os
import sys
#import socket
import platform
import subprocess
from os.path import expanduser
import sys, getopt

class bcolors:
	NC='\033[0m'
	Bold='\033[1m'
	Underlined='\033[4m'
	Blink='\033[5m'
	Inverted='\033[7m'
	Hidden='\033[8m'
	Black='\033[1;30m'
	Red='\033[1;31m'
	Green='\033[1;32m'
	Yellow='\033[1;33m'
	Blue='\033[1;34m'
	Purple='\033[1;35m'
	Cyan='\033[1;36m'
	LightGray='\033[1;37m'
	DarkGray='\033[1;30m'
	LightRed='\033[1;31m'
	LightGreen='\033[1;32m'
	LightYellow='\033[1;93m'
	LightBlue='\033[1;34m'
	LightPurple='\033[35m'
	LightCyan='\033[1;36m'

	White='\033[1;97m'
	BckgrDefault='\033[49m'
	BckgrBlack='\033[40m'
	BckgrRed='\033[41m'
	BckgrGreen='\033[42m'
	BckgrYellow='\033[43m'
	BckgrBlue='\033[44m'
	BckgrPurple='\033[45m'
	BckgrCyan='\033[46m'
	BckgrLightGray='\033[47m'
	BckgrDarkGray='\033[100m'
	BckgrLightRed='\033[101m'
	BckgrLightGreen='\033[102m'
	BckgrLightYellow='\033[103m'
	BckgrLightBlue='\033[104m'
	BckgrLightPurple='\033[105m'
	BckgrLightCyan='\033[106m'
	BckgrWhite='\033[107m'	
	#Typical format
	Achtung=LightRed+Bold+Blink
	Error=LightRed+Bold


param=dict()
rsyncoptions="--delete --delete-before --update --progress -t -a -r -v -E -h"


def SetPlatformDependentParameter():
	param['logmaster']=os.path.join(expanduser("~"),".backup","MASTER.txt")
	param['excludelist']=os.path.join(expanduser("~"),".backup","excludelist.txt")
	param['filepath']=os.path.join(expanduser("~"),".backup","harddrives.txt")
	if os.name=='nt':
		pass
	else:
		pass
		#linux

def init():
	SetPlatformDependentParameter()
	global logmaster
	import os.path
	if (os.path.isfile(logmaster)):
		os.remove(logmaster)
	log(param['logmaster'],"Backup starting",True)
	home = expanduser("~")	
	onofffile = str(home+"/.backup/OnOffStatus.txt")
	if (os.path.isfile(onofffile)):
		content = [line.rstrip('\n') for line in open(onofffile)]
		if content[0] == "off":
			log(param['logmaster'],onofffile+" contains off. Backup process is aborted",True)
			sys.exit(0)
		else:
			log(param['logmaster'],onofffile+" contains on. Backup process goes on",True)
	else:
		log(param['logmaster'],onofffile+" not found. Assuming backup process is wished. Process goes on",True)

def getDate():
	now = datetime.datetime.now()
	return now.strftime("%d-%m-%Y_%H-%M-%S")
	
def getLogForDrive(drivename):
	home = expanduser("~")
	return str(home+"/.backup/"+drivename+gedDate()+".log")

def log(logfile,string,printinstd):
	with codecs.open(logfile, 'a', encoding ='utf_8' ) as file:		#use a instead of w to append
		file.write("["+getDate()+"]"+string)
		file.write("\n")
	if printinstd==True:
		print(string)
				
def getPathToDisk(diskname):
	if os.name=='nt':
		return diskname
	else:
		return (str("/media/"+getpass.getuser()+"/"+diskname))

def getLastBackupDate(diskname):
	backupdatelistpath=os.path.join(getPathToDisk(diskname),"Backup","backup_date_list.txt")
	if (os.path.isfile(backupdatelistpath)):
		with open(backupdatelistpath) as f:
			content = [line.rstrip('\n') for line in open(backupdatelistpath)]	#while this approach does not
			return content[len(content)-1].split("_")[1]
	else:
		return "nofile"
	
def getMonthlyOrDaily(lastedate):
	try :
		if (int(lastedate)==int(datetime.datetime.now().month)):
			return "daily"
		else:
			return "monthly"
	except: 
		return "daily"

def AddTodayAsSaveDate(diskname):
	backupdatelistpath=getPathToDisk(diskname)+"/Backup/backup_date_list.txt"
	if (not os.path.isfile(backupdatelistpath)):
		with codecs.open(backupdatelistpath, 'w', encoding ='utf_8' ) as file:		#use a instead of w to append a+ to append/create w+ for write/create
			file.write("Liste of Backup date")
	with codecs.open(backupdatelistpath, 'a', encoding ='utf_8' ) as file:		#use a instead of w to append
		now = datetime.datetime.now()
		file.write("\n"+now.strftime("%d_%m_%Y"))

def getTarget(diskname,strategy):
	return os.path.join(getPathToDisk(diskname),"Backup",platform.node(),strategy)

def getSource():
	return (expanduser("~"))

def LaunchCopyCommand(source,target):
	if os.name=="nt":

		pass
	else:
		rsyncarg=rsyncoptions+" --exclude "+param['excludelist']+" "+source+" "+target
		rsyncarglist=rsyncarg.split(" ")
		spc=subprocess.Popen(["rsync"] + rsyncarglist,stdout=subprocess.PIPE)
		#stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL if you want to ignore every output
		out,err=spc.communicate()	#catch stdout and stderr
		outstr=out.decode(sys.stdout.encoding)	#out is a bytstring i.e 'b'blalbal\n'  while outstr now soleley contains blablala
		spc.wait()			#Wait until end (remove if you want parrall exec
		log(param['logmaster'],"rsync return code "+str(spc.returncode),True)
		log(param['logmaster'],"Will add the date to the backup date list",True)


def BackupOnADisk(diskname,argstrategy):
	global rsyncoptions
	log(param['logmaster'],"Will check if "+getPathToDisk(diskname),True)
	if(os.path.ismount(getPathToDisk(diskname))==False):
		log(param['logmaster'],"Harddrive "+diskname+" is not mounted",True)
		return 
	log(param['logmaster'],"Harddrive "+diskname+" is mounted",True)
	lastedate=getLastBackupDate(diskname)
	strategy=getMonthlyOrDaily(lastedate)
	strategy="daily" if argstrategy=="dailyonly" else strategy
	log(param['logmaster'],str("We have found the last month of backup: "+lastedate+". We will perform a "+strategy+" backup"),True)
	target=getTarget(diskname,strategy)
	source=getSource()
	if (os.path.isdir(target)==False):
		os.makedirs(target)
	log(param['logmaster'],"We will issue following command:\nrsync "+rsyncoptions+" --exclude "+param['excludelist']+" "+source+" "+target,True)
	LaunchCopyCommand(source,target)
	AddTodayAsSaveDate(diskname)
	
	
def getListOfHarddriveToBackup():
	with open(param['filepath']) as f:  #This conserve the \n at en of lines
		return [line.rstrip('\n') for line in open(param['filepath'])]
	



def usage():
	print(bcolors.LightRed +sys.argv[0] + bcolors.LightPurple+ '[-h -v --errocode -s --strategy -b --longargb]' +bcolors.NC)
	print(bcolors.LightGreen +"\tWhere:")
	print(bcolors.LightPurple +"\t-s|--strategy"+bcolors.LightCyan+"\tThe backup strategy")
	print(bcolors.LightPurple +"\t-b|--longargb"+bcolors.LightCyan+"\targb_description")
	print(bcolors.LightGreen +"\n\n\tDescription:")
	print(bcolors.LightCyan +"\tThis will backup the home folder on a harddrive \n\tstrategy:\n\t\t\"dailyonly\" means we simpy backup every time in a \"daily\" folder. \n\t\t\"dailyandmonthly\" means we apply dailyonly unless we are on the first day of the month where we will save in a \"monthly\" subfolder instead of a \"daily\" ")	
	print(bcolors.LightGreen +"\n\n\tExample of use:")
	print(bcolors.LightRed +"\t"+sys.argv[0] + bcolors.LightPurple+' --strategy '+bcolors.LightCyan+"dailyonly"+ bcolors.LightPurple+' --longargb '+bcolors.LightCyan+"exemplaargb")       
	print(bcolors.NC)
	
def errorlist():
	print(bcolors.Red+"--------------------------------------------------------")
	print("EXIT CODE       |MEANING")
	print("--------------------------------------------------------")
	print("0               |Success")
	print("1               |Error when parsing argument")
	print("255             |Exit returning information (help, version, list of error codes etc)"+bcolors.NC)

def CheckAndQuitUponFolderMissing(folderlist,errorcode):
	for folder in folderlist:
		if (not os.path.isdir(folder)):
			print(bcolors.LightRed+"Exit error code "+str(errorcode)+": folder "+folder+" does not exist"+bcolors.NC)
			sys.exit(errorcode)


		
def main(argv):
	argstrategy = ''
	varnameb = ''
	

	try:
		opts, args = getopt.getopt(argv,"hs:b:",["errorcode","strategy=","longargb="])
		
	except getopt.GetoptError:
		usage
		sys.exit(1)
		
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
			
		if opt == '--errorcode' :
			errorlist()
			sys.exit()
			
		elif opt in ("-s", "--strategy"):
			argstrategy = arg
			
		elif opt in ("-b", "--longargb"):
			varnameb = arg
	#Write the code below, bare in minde functions must be forwarde declared

	if argstrategy not in ['dailyonly', 'monthly']:
		argstrategy='dailyonly'
	print(argstrategy)	
	init()
	for drive in getListOfHarddriveToBackup():
		BackupOnADisk(drive,argstrategy)

if __name__ == "__main__":
        main(sys.argv[1:])
