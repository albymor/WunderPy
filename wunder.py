# !/usr/bin/python
# coding: utf-8

# Copyright 2017 Alberto Morato
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bs4 import BeautifulSoup as bs 
from optparse import OptionParser
import requests
import sys
import re
import json
import ast

reload(sys)
sys.setdefaultencoding('utf-8')

def get_page_content(id):
	# get the page content
	page_content = requests.get('https://www.wunderground.com/personal-weather-station/dashboard?ID=' + id).content
	return bs(page_content, "html.parser")

def get_current_data(id):
	# get the page content
	soup = get_page_content(id)

	#dict that will contain the weather parameters
	weather_condition = {}
	
	#find field containing weather data
	wx_data = soup.find_all("span", class_="wx-data")
	for data in wx_data:
		weather_condition["station_id"] = [data["data-station"].strip()]
		data_variable = data["data-variable"]
		#extract the actual data and measure unit
		spans = data.find_all("span")
		datas = []
		for span in spans:
			datas.append(span.text.strip())
		weather_condition[data_variable] = datas

	return weather_condition

def get_hystory(id):
	
	# get the page content
	soup = get_page_content(id)

	# find the part conining the table with all the parameters
	pattern = re.compile(r"wui.bootstrapped.pwsdashboard\s+=\s+.*")
	script = soup.find("script", text=pattern)

	# strip the header and the tail from the table
	remove_header_pattern = re.compile(r"wui.bootstrapped.pwsdashboard\s+=\s+")
	remove_last_pattern = re.compile(r";")
	data = re.sub(remove_header_pattern, "", script.text)#, re.IGNORECASE)
	data = re.sub(remove_last_pattern, "", data)

	#declaration of some variables needed to convert the table to a python dict
	null = None
	false = False
	true = True
	crossLinkingVars = "crossLinkingVars"
	histType = "histType"
	locid = "locid"
	radarCamVars = "radarCamVars"
	stationid = "stationid"
	units = "units"
	nwo = "nwo"
	sda = "sda"
	cam = "cam"
	nim  = "nim "
	pws_bootstrap = "pws_bootstrap"
	country = "country"
	mapTypeId = "mapTypeId"
	lat = "lat"
	lon = "lon"
	isRecent = "isRecent"
	lastUpdateEpoch = "lastUpdateEpoch"
	units = "units"
	mode = "mode"
	scrollTo = "scrollTo"

	# convert the table to a python dict
	data_dict = eval(data)
	return data_dict

def print_data(weather_data):
	for key in weather_data:
		print key + ': ' + ' '.join([v for v in weather_data[key]])

def main(argv):
	parser = OptionParser()

	parser.add_option(
		"-p", "--print", dest="print_opt", help="print fetched data", default=False, action="store_true")

	parser.add_option(
		"-d", "--dict", dest="dict_opt", help="return a dict with history fetched data", default=False, action="store_true")

	parser.add_option(
		"-i", "--id", dest="station_id",
		help="id of the station", default="IASIAGO1380")

	parser.add_option(
		"-o", "--output", dest="output_file", help="output file (not yet implemented)")

	(options, args) = parser.parse_args(sys.argv)

	if options.print_opt:
		print_data(get_current_data(options.station_id))

	if options.dict_opt:
		tmp = get_hystory('IASIAGO1380')
		# print tmp["radarCamVars"]["pws_bootstrap"]["history"]["days"]["observations"]
		for measure in tmp["radarCamVars"]["pws_bootstrap"]["history"]["days"][0]["observations"]:
			print measure
			print "---------------------------------------------------------------------------------"

if __name__ == '__main__':
	main(sys.argv)