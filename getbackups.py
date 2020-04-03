#!/usr/bin/python3
import os
import subprocess
import datetime
import time

#List of Instances ID=====

Command=" nova list --minimal | awk -F'|' '/\|/ && !/ID/{system(\"echo \"$2\"\")}'"
ListOfInstances = subprocess.Popen([Command], stdout=subprocess.PIPE, shell=True)
(output, err) = ListOfInstances.communicate()
output=str(output)
output=output.replace("b'","")
output=output.replace("'"," ")
output=output.replace(chr(92)+"n",' ')
ListOfInstances=output.split()

#Backup=====
#BackupType can be "daily" or "weekly" too 
BackupType="manual"
#Int parameter representing how many backups to keep around
Rotation="7"

ListOfOutputs = []
log = ""
for ID in ListOfInstances:
    #Name of the backup image
    Command = "echo 'Start OpenStack snapshot creation for instance ID'"+ID
    os.system(Command)
    Now = datetime.datetime.now()
    Now=str(Now)
    Now = Now.replace(" ","-")
    NameOfBackupImage=Now+ID
    Command ="nova backup "+ ID +" "+NameOfBackupImage+" "+ BackupType +" "+Rotation
    x = subprocess.Popen([Command], stdout=subprocess.PIPE, shell=True)
    (output, err) = x.communicate()
    output = str (output)
    output=output.replace("b'","")
    log = output + log + "\n"
    
    #If the number of your instances is high, backups may need to be delayed a bit
    time.sleep(3)


#Report=====
EmailFrom = "senderemail"
EmailTo = "youremail"

#Mailx must be pre-installed
Command = " mail -s \"Logs of backups instances\" -r \"" + EmailFrom + "\" \"" + EmailTo + "\""
os.system(Command)
