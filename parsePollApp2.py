import subprocess
import sys
import json
from tabulate import tabulate

# action, trigger, and rule ("functions") constants mapping to actual strings used in OpenWhisk
UPLOAD_N_DOCS = "uploadNDocs"
DB_CHANGE_RULE = "fileUploadedRuleLimit"
DB_CHANGE_TRIGGER = "cloudantChangeLimit"
DOC_UPLOADED = "docUploaded"

POST = "post"
GIT = "myGitActionJS"
GIT_TRIGGER = "myGitTrigger2"
GIT_RULE = 

# this is for analyzing if a trigger/rule could be created to only track file uploads. It is not an actual OpenWhisk function. The idea was to have a trigger fire every time a document was updated. Then docUploaded would be invoked every time the output file was updated but docUploaded would immediately exit. This would allow for comparison of having a "null" function being invoked as many times as a regular function was being invoked. Because OpenWhisk couldn't scale, this test ended up not making sense.
DOC_UPLOADED_WITHOUT_UPDATES = "docUploadedWithoutDocUpdates"

functionNames = [DB_CHANGE_RULE, DB_CHANGE_TRIGGER, DOC_UPLOADED, DOC_UPLOADED_WITHOUT_UPDATES]

# initialize dictionaries
invocations = {} # key = function; value = # of times invoked
runtimes = {} # key = function; value = ms spent running
for f in functionNames:
    invocations[f] = 0
    if f == UPLOAD_N_DOCS or f == DOC_UPLOADED or f == DOC_UPLOADED_WITHOUT_UPDATES:
        runtimes[f] = 0

file = open(sys.argv[1],'r')

def timeSpentRunning(startTime,endTime):
    if startTime > 0 and endTime > 0:
        differenceInMS = endTime - startTime
        if differenceInMS < 0:
            raise Error("time difference < 0 for doc uploaded")
        return differenceInMS
    else:
        raise Error("start time or end time is <= 0 for doc uploaded")

lines = 0
chars = 0
totalElapsedServerTime = 0
overallStart = 0 # this will be min start time found of all start times
overallEnd = 0 # this will be the max end time found of all end times
startCommand = []
endCommand = []
for line in file:
    parts = line.split(' ')
    if len(parts) == 3:
        invocations[parts[1]] += 1
        activationID = parts[2][1:-2]
        response = ""
        while response == "":
            try:
                response = subprocess.check_output("wsk activation get %s" % activationID, shell=True)
            except subprocess.CalledProcessError:
                print "wsk failed to get activation... trying again..."
        if "ok: got activation" in response:
            response = response.split('\n')[1:]
            response = '\n'.join(response)
            responseJSON = json.loads(response)
            startTime = responseJSON["start"]
            endTime = responseJSON["end"]
            if overallEnd < endTime:
                overallEnd = endTime
            if overallStart > startTime or overallStart == 0:
                overallStart = startTime
            
            if UPLOAD_N_DOCS == parts[1]:
                runtimes[UPLOAD_N_DOCS] += timeSpentRunning(startTime,endTime)
                if overallEnd < endTime:
                    overallEnd = endTime
                if overallStart > startTime or overallStart == 0:
                    overallStart = startTime
        
            elif DOC_UPLOADED == parts[1]:
                timeSpent = timeSpentRunning(startTime,endTime)
                runtimes[DOC_UPLOADED] += timeSpent
                
                # check if it's an upload
                result = responseJSON["response"]["result"]
                if "stats" in result.keys():
                    invocations[DOC_UPLOADED_WITHOUT_UPDATES] += 1
                    runtimes[DOC_UPLOADED_WITHOUT_UPDATES] += timeSpent
                    
                    statsJSON = json.loads(result["stats"])
                    lines += int(statsJSON["lines"])
                    chars += int(statsJSON["chars"])

for f in functionNames:
    row = []
    print "\n-----------\n" + f + "\n-----------"
    if f == UPLOAD_N_DOCS or f == DOC_UPLOADED or f == DOC_UPLOADED_WITHOUT_UPDATES:
        # TODO: cost
        avgTime = float(runtimes[f]) / float(invocations[f])
        row = [invocations[f],0,runtimes[f],avgTime]
    else:
        row = [invocations[f],"--","--","--"]
    print tabulate([row], headers=["Invocations", "Cost","Total Time","Time per Invocation"])

totalElapsedServerTime = overallEnd - overallStart

print "lines, chars, total elapsed time"

print lines
print chars
print totalElapsedServerTime






