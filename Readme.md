#Backup

Backup is a script that backs-up a user home directory at computer shutdwn.
It is aimed to work on Windows and On Linux

#Pre-requisites
## Windows
You need following packages
* Python 3
* Execution policies must be set to remote signed
* Cygwin and rsync (use the cygwing installer to install rsync)

## Linux 
* Python3
* rsync


# How to set up
# Windows 
1. Type Windows+R
2. Enter gpedit.msc
3. Computer Configuration / Windows Parameters / Start/Shutdown scripts
4. Add the Wraaper (the powershell script) as a shutodnw script. Make sure inside the wrapper you point to the correct location of backup.py

# Linux - KDE 
1. Go to system settings 
2. Enter startup/shutdown script in the searchbar