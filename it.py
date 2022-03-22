#MIDN STRYKER // 226342
#LAB5: program that can detect new, missing, or modified files on a system
#Modify the path argument in line 18 as needed
#take note that this should be run in same directory as the "log" file (old.txt)

import os
import os.path
import hashlib
import datetime

#Sources:
#https://www.tutorialspoint.com/python/os_walk.htm
#https:///www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
#https://www.geeksforgeeks.org/how-to-compare-two-text-files-in-python/
#BeagleD on Github (Prof Dias)

banned = ['sys','proc','run','dev','var/lib','var/run','tmp']
#the "../../" argument can be changed to wherever you wanna start/where its being run
for root, dirs, files in os.walk("../../",topdown=False): #start at top
    
    for name in files: #loop through files
        fileName = os.path.join(root,name)
        #print(os.path.join(root,name)) #name
        flag=0
        for ban in banned:
        	if ban in fileName:
        		flag = 1
        if flag == 1:
        	continue

        try: 
            sha256_hash = hashlib.sha256() #set up sha256
            with open(os.path.join(root,name),"rb") as f: #open file and hash it
                for byte_block in iter(lambda: f.read(4096),b""):
                    sha256_hash.update(byte_block)
                    theHash = sha256_hash.hexdigest() #the hash
        except:
            None
        if len(theHash) <= 1:
            theHash = 'no hash found'
        dateTime = datetime.datetime.now() #the current date time
        
        #Current state
        with open("tmp.txt","a") as tmp:
            theString = fileName+' '+theHash+' '+str(dateTime)+'\n'
            tmp.write(theString) #name
        
        #Compare the current state with the "old" state
        #*************Name "old" state old.txt*****************
if os.path.exists("./old.txt") == True:
    new = open("tmp.txt","r")
    old = open("old.txt","r")
    i = 0
    #MAKE DICTIONARIES
    newLDict = {}
    oldLDict = {}
    for newL in new:
    	newLList = newL.split()
    	#print(newLList)
    	newLDict[newLList[0]]=newLList[1] #dictionary with file:hash
    for oldL in old:
        oldLList = oldL.split()
        oldLDict[oldLList[0]]=oldLList[1] #dictionary with file:hash
    for fileName in oldLDict: #MISSING FILES?
        if fileName not in newLDict:
            print("MISSING FILE:", fileName)
    for fileName2 in newLDict: #NEW FILES?
    	if fileName2 not in oldLDict:
            print("NEW FILE:", fileName2)    	                      
            continue
    	if newLDict[fileName2] != oldLDict[fileName2]: #MODIFIED?
            print("MODIFIED FILE:", fileName2)
    new.close()
    old.close()    	            
    os.system("rm old.txt")

os.system('mv tmp.txt old.txt') #preparing next iteration            	
                          
        
	
  
