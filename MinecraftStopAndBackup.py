#Title: Minecraft Server Shutdown and Backup Automation
#Created by: Chris Tudehope
#Description: This program automates the operation of shutting down and backing up a
#Minecraft server by copying the world folder. 
import autoit
import time
from Backup import backupServer

#This function will check if a Minecraft server is running. If so it will send a countdown
#to any players on the server and then shut the server down. The function uses autoit to 
#inject commands into the Minecraft server's command prompt.
#Return
#	boolean: Returns true if server is shutdown. Return false if error occured
def serverShutdown():
	ret = False
	if autoit.win_exists("C:\Windows\system32\cmd.exe"):	#Checks if the window Minecraft would be in is currently running
		print("The Minecraft server was found and will be shut down in 30 seconds.")
		#Note: The following command brings the Minecraft command prompt to the front.
		#It will be run after any pause just in case a user activates another screen some point
		#during that pause.
		autoit.win_activate("C:\Windows\system32\cmd.exe")
		autoit.send("say The server will be shutting down in 30 seconds.")
		autoit.send("{Enter}")
		for s in range(30,-1,-1):
			time.sleep(1)
			if(s == 15 or s == 10 or (s <= 5 and s >= 3)):
				autoit.win_activate("C:\Windows\system32\cmd.exe")
				autoit.send("say " + str(s) + " seconds till shutdown{!}")
				autoit.send("{Enter}")
			elif(s == 2):
				autoit.win_activate("C:\Windows\system32\cmd.exe")
				autoit.send("say " + str(s) + " seconds till shutdown{!}{!}{!}")
				autoit.send("{Enter}")
			elif(s == 1):
				autoit.win_activate("C:\Windows\system32\cmd.exe")
				autoit.send("say " + str(s) + " SECOND TILL SHUTDOWN{!}{!}{!}{!}{!}")
				autoit.send("{Enter}")
		print("Server is shutting down.")			
		autoit.win_activate("C:\Windows\system32\cmd.exe")
		autoit.send("say Server is shutting down now{!}")
		autoit.send("{Enter}")
		autoit.send("stop")
		autoit.send("{Enter}")
		#sleep to give the server time to shutdown
		time.sleep(5)
		#Log to console whether server is stopped
		if autoit.win_exists("C:\Windows\system32\cmd.exe") == False:
			print("The Minecraft server was successfully shutdown!")
			ret = True
		else:
			print("Error: The stop command was sent but the server is still found!")
			ret = False
	else:	#Minecraft instance was not found
		print("The server was not found.")
		ret = True		#Return true because this function only needs to make sure the server is off
	return ret


#Start of program
if serverShutdown() == True:	#Check if server was shut down
	backupSrc = "E:\\ServerForThePlex\\world"	
	backupDest = "C:\\MinecraftBackups\\"
	print("Minecraft Backup is in Progress. It takes awhile :(")
	if backupServer(backupSrc,backupDest,15) == True:	#Check if backup occurred
		print("A backup was created in the folder: " + backupDest)
		#Give the user time to see final console output
		time.sleep(5)
	else:
		print("Backup aborted because of server backup error.")
		#Give the user time to see final console output
		time.sleep(10)
else:
	print("Backup aborted because of server shutdown error.")
	#Give the user time to see final console output
	time.sleep(10)
	