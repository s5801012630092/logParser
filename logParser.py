import json         # For Json Convert
import re           # For Regular Expression
from PIL import Image,ImageTk
import urllib.request
import os

from tkinter import *
from tkinter.filedialog import askopenfilename

# For draw pie chart 
import matplotlib.pyplot as plt

#google_api_key = "AIzaSyAuJuxmyP1g-HJPhzp4WZ_Vpldv6qYGQk4"

def parse_json(filepath):
	try:
		with open(filepath) as f:
			data = json.load(f);
		return True
	
	except ValueError as e:
		print('invalid json: %s' % e)
		return False

def convert_to_json(filename_1):
	# Convert access_log to JSON File and add information
		output_file = "data.json"
		count_dict = {}
		is_json = False
		old_info_keys = []
		# del if output_file is exist.
		if os.path.isfile(output_file) :
				pass

				# Validate json file
				if parse_json(filename_1) == True:
						is_json = True
				else:
						is_json = False

				#is_json = False
				
				if is_json == True :
						# read file
						with open(output_file) as fd:
								json_data = json.load(fd)

						# get all data_ip to info
						old_info = (json_data["information"][0])
				
						# get all ip
						old_info_keys = list(json_data["information"][0])

						# set all info to count_dict
						for i in range(0 ,len(old_info_keys) - 1 ):
								count_dict[old_info_keys[i]] = old_info[ old_info_keys[i] ]

						# get all protocal
						old_protocal = json_data["ips"]

						# and Del after collenct data
						os.remove(output_file)

				else:
						# Del if file is incurrent
						os.remove(output_file)

						# Then Call itself
						convert_to_json(filename_1)
		else:
				pass
		
	# Write Data Part
		# Read access_log File
		# Open a log file
		access_log_file = open(filename_1, "r+") #"access_log"

		# Write Head
		head = "ips"
		with open(output_file, 'a') as json_file:
				json_file.write("{\"" + head + "\": [  ")

		# Write data from json file
		#aaa
		if is_json == True:
				for i in range(0 ,len(old_protocal)-1):
						data = {
								'ip'           : old_protocal[i]['ip'],
								'ident'        : old_protocal[i]['ident'],
								'userid'       : old_protocal[i]['userid'],

								'day'          : old_protocal[i]['day'],
								'month'        : old_protocal[i]['month'],
								'year'         : old_protocal[i]['year'],
								'hour'         : old_protocal[i]['hour'],
								'minute'       : old_protocal[i]['minute'],
								'second'       : old_protocal[i]['second'],
								'timezone'     : old_protocal[i]['timezone'],
		   
								'protocol'     : old_protocal[i]['protocol'],
								'status code'  : old_protocal[i]['status code'],
								'last entry'   : old_protocal[i]['last entry']
								}

						# Write Data Part
						with open(output_file, 'a') as json_file:
								json.dump(data, json_file)
								json_file.write(",")

		# Read and Convert access file to json 
		while True:
				# Read Part
				line = access_log_file.readline()
				# Cancel Read and Exit when no line to read
				if not line:
						# Write Del last character (",")
						with open(output_file, 'rb+') as json_file:
								json_file.seek(0,2)                 # to end of file
								size = json_file.tell()             # get size
								json_file.truncate(size-1)          # cut 1 charecter from last
						break
			# Convert Part
				# 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
				# Format
				# {ip} {ident} {userid} [{day}/{mouth}/{year}:{hour}:{min}:{sec} {tzone}] "{protocol}" {statuscode} {byte}
				regex = re.match("(.*) (.*) (.*) \[(.*)\/(.*)\/(.*):(.*):(.*):(.*) (.*)\] \"(.*)\" (.*) (.*)\\n", line)
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
								'last entry'   : regex.group(13)
								}	
						# Count Part
						key = regex.group(1)
						if key in count_dict:
								count_dict[key] = count_dict[key] + 1
						else :
								count_dict[key] = 1			
				else:
						print ("No match!!")
				# Write Data Part
				with open(output_file, 'a') as json_file:
						json.dump(data, json_file)
						json_file.write(",")
		# Write End 
		with open('data.json', 'a') as json_file:
				json_file.write("]")

	# Write Information Part
		# Write Head
		head = "information"
		with open(output_file, 'a') as json_file:
				json_file.write(",\"" + head + "\": [  ")
		# Download infomation
		for key, value in count_dict.items():
				if (key in old_info_keys) or (not old_info_keys) :
						# Write Open 
						url_data = "http://ip-api.com/json/" + key
						res = urllib.request.urlopen( url_data )
						res_body = res.read()
						j = json.loads(res_body.decode("utf-8"))
						data_map = j
						if data_map["status"] == "success":
								data = {
										'ip'            : key,
										'call'          : value,
										'address'       : data_map["as"],
										'city'          : data_map["city"],
										'country'       : data_map["country"],
										'countryCode'   : data_map["countryCode"],
										'isp'           : data_map["isp"],
										'lat'           : data_map["lat"],
										'lon'           : data_map["lon"],
										'org'           : data_map["org"],
										'query'         : data_map["query"],
										'region'        : data_map["region"],
										'regionName'    : data_map["regionName"],
										'status'        : data_map["status"],
										'timezone_area' : data_map["timezone"],
										'zip'           : data_map["zip"]
								}
								print("S")
						elif data_map["status"] == "fail":
								data = {
										'call'          : value,
										"message"       : "invalid query",
										"query"         : "lj1120.inktomisearch.com",
										"status"        : "fail"
								}
								print("F")
						else:
								pass
						# Write Information
						with open(output_file, 'a') as json_file:
								json.dump(data, json_file)
								json_file.write(",")
				else:
						pass

		# Write Del last character (",")
		with open(output_file, 'rb+') as json_file:
				json_file.seek(0,2)                 # to end of file
				size = json_file.tell()             # get size
				json_file.truncate(size-1)          # cut 1 charecter from last (",")
						
		# Write End 
		with open('data.json', 'a') as json_file:
				json_file.write("]")

		# Write End JSON
		with open('data.json', 'a') as json_file:
				json_file.write("}")
		
		# Close opend file
		access_log_file.close
		json_file.close

		print ("Totel AD : " + str(len(count_dict)))

def get_mouth_number(month):
	# For change string to int. eg. Jan is 1
	if month == "Jan":
			return 1
	if month == "Feb":
			return 2
	if month == "Mar":
			return 3
	if month == "Apr":
			return 4
	if month == "May":
			return 5
	if month == "Jun":
			return 6
	if month == "Jul":
			return 7
	if month == "Aug":
			return 8
	if month == "Sep":
			return 9
	if month == "Oct":
			return 10
	if month == "Nov":
			return 11
	if month == "Dec":
			return 12
	else:
			return 0

def top_dic(dic ,top):
	# For sort top10 of ip.
	return (sorted(dic, key=dic.get, reverse=True)[:top])

class SetGUI:
	""" set canvas
		open file function
		search by date function
		show top10 list
		show map function
		show chart function """

	def __init__(self, master):
		self.master = master
		master.title("Python Program : World Map")
		master.geometry("1200x750")
		self.filename = "data.json"
		
		self.label_1 = Label(master, text="Choose file json")
		self.label_1.place(x=640,y=20)

		self.file_button_1 = Button(master, text="Choose file", command=self.json_file)
		self.file_button_1.place(x=640,y=40)
		
		self.label_2 = Label(master, text="Choose file to convert")
		self.label_2.place(x=640,y=80)
		
		self.file_button_2 = Button(master, text="Convert file", command=self.convert_file)
		self.file_button_2.place(x=640,y=100)
		
		self.label_3 = Label(master, text="Choose Date (dd/mm/yyyy)")
		self.label_3.place(x=840,y=20)
		
		self.textBox_3 = Text(master, height=1, width=10)
		self.textBox_3.place(x=840,y=50)
		
		self.label_4 = Label(master, text="to")
		self.label_4.place(x=940,y=50)
		
		self.textBox_4 = Text(master, height=1, width=10)
		self.textBox_4.place(x=960,y=50)
		
		self.file_button_3 = Button(master, text="Enter Date", command=self.search_by_date)
		self.file_button_3.place(x=1100,y=45)

		self.label_5 = Label(master, text="", justify=LEFT)
		self.label_5.place(x=840,y=100)

		self.top10_ip = []		# stored list top10 of ip
		self.top10_call = []	# stored list top10 of call
		self.get_lat = []		# stored list latitude
		self.get_lon = []		# stored list longtitude

	def convert_file(self):
		# For convert log file to json
		filename = askopenfilename()
		convert_to_json(filename)
		
	def json_file(self):
		""" For open json file and put the data
				=> all ip when open file
				=> ip call
				=> latitude longtitude of all ip.
			And call show map and chart function """

		# open json file
		self.filename = askopenfilename()
		
		dic_ip_call = {} # to stored ip(key) and call(value)
		lat = None
		lon = None
		
		# call json file
		with open(self.filename) as fd:
			json_data = json.load(fd)
			
		# get all ip to keys list and info_keys list
		keys = list(json_data["information"][0])
		info      = (json_data["information"][0])
		info_keys = list(json_data["information"][0])

		# put number call , lat ,lon in dictionary that has ip(keys)
		for i in range(0,len(keys)-1):
			dic_ip_call[keys[i]] = json_data["information"][0][keys[i]][0]["call"]
		# set self.get_lat and self.get_lon to empty list
		self.get_lat = []
		self.get_lon = []
		# loop for append latitude and longtitude in list
		for i in range(0,len(info_keys)):
			ip = info_keys[i]
			if info[ip][0]["status"] == "fail":
				lat = 0
				lon = 0
			if info[ip][0]["status"] == "success":
				self.get_lat.append(float(info[ip][0]["lat"]))
				self.get_lon.append(float(info[ip][0]["lon"]))

		# put top 10 most ip called to list_top10 list
		list_top10 = top_dic(dic_ip_call ,10)

		top10detail = ""
		# set self.top10_ip and self.top10_call to empty list
		self.top10_ip = []
		self.top10_call = []
		# loop for print text top10 ip with call and append ip and call to list for chart
		for i in range(0,10):
			top10detail = top10detail + str(i+1) +" : " + list_top10[i] + " : " + str(dic_ip_call[list_top10[i]])+"\n"
			self.top10_ip.append(list_top10[i])
			self.top10_call.append(int(dic_ip_call[list_top10[i]]))		
		# call show_map_chart function to show map and chart with list that appended
		self.show_map_chart()
		self.label_5['text'] = top10detail

	def search_by_date(self):
		input_before = self.textBox_3.get("1.0",END)
		search_day_before   = input_before.split("/")[0]
		search_month_before = input_before.split("/")[1]
		search_year_before  = input_before.split("/")[2][:-1]  # del "\n"
		input_after  = self.textBox_4.get("1.0",END) #end-1c
		search_day_after    = input_after.split("/")[0]
		search_month_after  = input_after.split("/")[1]
		search_year_after   = input_after.split("/")[2][:-1]  # del "\n"

		dic_ip_call = {}
		ip_search = []
						
		# read file
		with open(self.filename) as fd:
				json_data = json.load(fd)

		# get all data_ip to info
		info = (json_data["information"][0])
		info_keys = list(json_data["information"][0])
		
		# put all ip & number call to dic_ip_call
		keys = list(json_data["information"][0])
		
		# search top10 in date
		protocal = json_data["ips"]
		
		for i in range(0 ,len(json_data["ips"])):
			if (    int(json_data["ips"][i]['day'])                >= int(search_day_before)
				and int(json_data["ips"][i]['day'])                <= int(search_day_after)
				and get_mouth_number(json_data["ips"][i]['month']) >= int(search_month_before)
				and get_mouth_number(json_data["ips"][i]['month']) <= int(search_month_after)
				and int(json_data["ips"][i]['year'])               >= int(search_year_before)
				and int(json_data["ips"][i]['year'])               <= int(search_year_after)) :
	
				# Count Part
				if json_data["ips"][i]['ip'] in dic_ip_call:
					dic_ip_call[json_data["ips"][i]['ip']] = dic_ip_call[json_data["ips"][i]['ip']] + 1
				else :
					dic_ip_call[json_data["ips"][i]['ip']] = 1
		for key in dic_ip_call.keys():
			ip_search.append(key)

		self.get_lat = []
		self.get_lon = []
		for i in range(0,len(ip_search)):
			for j in range(0,len(info_keys)):
				if info_keys[j] == ip_search[i]:
					ip = ip_search[i]
					if info[ip][0]["status"] == "success":
						self.get_lat.append(float(info[ip][0]["lat"]))
						self.get_lon.append(float(info[ip][0]["lon"]))
						# print (self.get_lat)
						# print (self.get_lon)
					else:
						lat = 0
						lon = 0

		# put top 10 most ip called to list_top10 list
		list_top10 = top_dic(dic_ip_call ,10)

		self.top10_call = []
		self.top10_ip = []
		# set string to print
		top10detail = ""
		for i in range(0,10):
			top10detail = top10detail + str(i+1) +" : " + list_top10[i] + " : " + str(dic_ip_call[list_top10[i]])+"\n"
			self.top10_ip.append(list_top10[i])
			self.top10_call.append(int(dic_ip_call[list_top10[i]]))
		
		self.show_map_chart()
		self.label_5['text'] = top10detail

	def show_map_chart(self):
		""" Draw map and pie chart """
		# Draw map
		import matplotlib
		matplotlib.use('TkAgg')
		from mpl_toolkits.basemap import Basemap
		from matplotlib.figure import Figure
		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
		import sys
		if sys.version_info[0] < 3:
			import Tkinter as Tk
		else:
			import tkinter as Tk
		# Draw a map and embbed base map in tk.
		fig = Figure()
		ax1 = fig.add_subplot(111)
		# world map style
		m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
								llcrnrlon=-180,urcrnrlon=180,resolution='c',ax=ax1)
		m.drawmapboundary(fill_color='#99ccff')
		m.fillcontinents(color='#c68c53',lake_color='#99ccff')
		# plot latitude and longtitude
		x,y = m(self.get_lon, self.get_lat)
		m.plot(x, y, 'b.', markersize=5)
		# make empty canvas and draw map in there
		canvas = FigureCanvasTkAgg(fig, master=root)
		canvas.show()
		canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		canvas._tkcanvas.place(x=0,y=0)

		# Draw pie chart
		labels = self.top10_ip
		sizes = self.top10_call
		fig2 = Figure()
		ax2 = fig2.add_subplot(111)
		patches,texts,autotexts = ax2.pie(sizes, autopct='%1.1f%%',
				startangle=90)
		ax2.legend(labels, loc="best",prop={'size': 6})
		# Set size of text in chart
		for t in texts:
			t.set_size('smaller')
		for t in autotexts:
			t.set_size('x-small')
		ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		# make empty canvas and draw pie chart in there
		canvas2 = FigureCanvasTkAgg(fig2, master=root)
		canvas2.show()
		canvas2.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		canvas2._tkcanvas.place(x=640,y=300)

# Call Tkinter and call function to show map and chart.
root = Tk()
my_gui = SetGUI(root)
my_gui.show_map_chart()
root.mainloop()