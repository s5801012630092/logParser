# This is Liblary
import json         # For Json Convert
import re           # For Regular Expression
import urllib.request
from tkinter import *
from PIL import Image,ImageTk


google_api_key = "AIzaSyAuJuxmyP1g-HJPhzp4WZ_Vpldv6qYGQk4"

# (1) Convert access_log to JSON File
"""
# Read access_log File

# Open a file
access_log_file = open("access_log", "r+")

# Write Head
head = "ips"

with open('data.json', 'a') as json_file:
    json_file.write("{\"" + head + "\": [  ")

# Read and Convert access file to json
while True:

    # Read Part
    line = access_log_file.readline()


    # Cancel Read and Exit when no line to read
    if not line:
        # Write Del last character (",")
        with open('data.json', 'rb+') as json_file:
            json_file.seek(0,2)                 # to end of file
            size = json_file.tell()             # get size
            json_file.truncate(size-1)          # cut 1 charecter from last
        break
        
    # Convert Part
    
    # 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
    # Format
    # {ip} {ident} {userid} [{day}/{mouth}/{year}:{hour}:{min}:{sec} {tzone}] "{protocol}" {statuscode} {byte}

    
    
    regex = re.match("(.*) (.*) (.*) \[(.*)\/(.*)\/(.*):(.*):(.*):(.*) (.*)\] \"(.*)\" (.*) (.*)\\n", line)

    #print (line)

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

        
    # Write Data Part
    with open('data.json', 'a') as json_file:
        json.dump(data, json_file)
        json_file.write(",")

with open('data.json', 'a') as json_file:
    json_file.write("]}")
    
# Close opend file
access_log_file.close
json_file.close
"""


# (2) Read data from data.json

with open('data.json') as fd:
     json_data = json.load(fd)

     
# (3) GUI Part

now_ip = " "

root = Tk()

root.title("Python Program : Find Address")
root.geometry("800x600")


for i in range (1 ,len(json_data["ips"])):

    # Call image data
    url_data = "http://ip-api.com/json/" + json_data["ips"][i]["ip"]
    
    res = urllib.request.urlopen( url_data )
    res_body = res.read()
    j = json.loads(res_body.decode("utf-8"))
    
    data_map = j
    
    
    if now_ip == data_map["query"]: #False:#
        pass
    else:
    
        if data_map["status"] == "success":
            # Download Image from google map
            url_map = "https://maps.googleapis.com/maps/api/staticmap?center=" + str(data_map["lat"]) + "%2c%20" + str(data_map["lon"]) +"&zoom=12&size=400x400&key=" + google_api_key
            urllib.request.urlretrieve(url_map , "success.png")
        
            # Load Image and data
            load = Image.open("success.png")
            render = ImageTk.PhotoImage(load)

            img = Label(root, image=render)
            img.image = render
            img.place(x=20, y=20)

            text = Label(root, text="line : " + str(i))
            text.place(x=720, y=20)
            text = Label(root, text="IP      : " + data_map["query"])
            text.place(x=480, y=20)
            text = Label(root, text="Status : " + data_map["status"])
            text.place(x=480, y=55)
            text = Label(root, text="Address  : " + data_map["as"])
            text.place(x=480, y=90)
            text = Label(root, text="City  : " + data_map["city"])
            text.place(x=480, y=110)
            text = Label(root, text="Region  : " + data_map["regionName"])
            text.place(x=480, y=130)
            text = Label(root, text="Country  : " + data_map["country"])
            text.place(x=480, y=150)
            text = Label(root, text="Latitude  : " + str(data_map["lat"]))
            text.place(x=480, y=170)
            text = Label(root, text="Longtitude : " + str(data_map["lon"]))
            text.place(x=480, y=190)
            text = Label(root, text="Date : "+json_data["ips"][i]["hour"]+":"+json_data["ips"][i]["minute"]+":"+json_data["ips"][i]["second"]+" "+json_data["ips"][i]["day"] +"/"+ json_data["ips"][i]["month"] +"/"+ json_data["ips"][i]["year"])
            text.place(x=480, y=220)
            
        elif data_map["status"] == "fail":

            # Load Image and data
            load = Image.open("fail.png")
            render = ImageTk.PhotoImage(load)

            img = Label(root, image=render)
            img.image = render
            img.place(x=20, y=20)
        
            text = Label(root, text="line : " + str(i))
            text.place(x=720, y=20)
            text = Label(root, text="IP      : " + data_map["query"])
            text.place(x=480, y=20)
            text = Label(root, text="Status : " + data_map["status"])
            text.place(x=480, y=55)
            text = Label(root, text="Date : " + str(data_map["lon"]))
            text.place(x=480, y=220)
        else:
            pass
    
    var = IntVar()
    button = Button(root, text="Next ", command=lambda: var.set(1))
    button.place(x=520, y=260)

    button.wait_variable(var)

    now_ip = data_map["query"]
    


#root.mainloop()  
















































