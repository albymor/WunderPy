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

reload(sys)
sys.setdefaultencoding('utf-8')

def fetch_data(id):

	# get the page content
	page_content = requests.get('https://www.wunderground.com/personal-weather-station/dashboard?ID=' + id).content
	soup = bs(page_content, "html.parser")
	
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

def print_data(weather_data):
	for key in weather_data:
		print key + ': ' + ' '.join([v for v in weather_data[key]])

def main(argv):
	parser = OptionParser()

	parser.add_option(
		"-p", "--print", dest="print_opt", help="print fetched data", default=False, action="store_true")

	parser.add_option(
		"-i", "--id", dest="station_id",
		help="id of the station", default="IASIAGO1380")

	parser.add_option(
		"-o", "--output", dest="output_file", help="output file (not yet implemented)")

	(options, args) = parser.parse_args(sys.argv)

	if options.print_opt:
		print_data(fetch_data(options.station_id))

if __name__ == '__main__':
	main(sys.argv)