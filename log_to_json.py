# This is Liblary
import json
import re
# import rhinoscriptsyntax as rs

# Read access_log File
# Open a file
access_log_file = open("access_log", "r+")
# Read and Convert access file to json
while True:
    # Read Part
    line = access_log_file.readline()
    # Cancel Read and Exit when no line to read
    if not line: 
        break    
    # Convert Part
    # 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
    # Format
    # {ip} {ident} {userid} [{day}/{mouth}/{year}:{hour}:{min}:{sec} {tzone}] "{protocol}" {statuscode} {byte}
    regex = re.match("(.*) (.*) (.*) \[(.*)\/(.*)\/(.*):(.*):(.*):(.*) (.*)\] \"(.*)\" (.*) (.*)\\n", line)
    print (line)
    if regex:
        data = {
            'ip'           : regex.group(1),
            'ident'        : regex.group(2),
            'userid'       : regex.group(3),

            'day'          : regex.group(4),
            'month'        : regex.group(5),
            'year'         : regex.group(6),
            'hour'         : regex.group(7),
            'minute'       : regex.group(8),
            'second'       : regex.group(9),
            'timezone'     : regex.group(10),
       
            'protocol'     : regex.group(11),
            'status code'  : regex.group(12),
            'last entry'   : regex.group(13)     }
    
    else:
        print ("No match!!")

    # Write Part
    with open('data.json', 'a') as json_file:
        json.dump(data, json_file)
        json_file.write("\n")

# Close opend file
access_log_file.close
json_file.close

# GUI Part