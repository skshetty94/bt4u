import argparse
import requests
import json
from bs4 import BeautifulSoup

def get_data_from_url(url, html_content_key):
		r = requests.get(url)
		try:
			json_data = json.loads(r.content[1:-1])
			html_content = json_data[html_content_key]
			return BeautifulSoup(html_content, "html.parser")
		except:
			return None

def get_route_id(all_routes_url):
	soup = get_data_from_url(all_routes_url, "routeListHtml")
	routes = soup.find_all("a", "list-group-item")
	print "Applicable route ids: "
	for r in routes:
		print r.attrs['data-routes'].split('|')[0]
		
all_routes_url = "https://commonlayer.bt4u.org/routes"
parser = argparse.ArgumentParser(description= get_route_id(all_routes_url))
parser.add_argument('route_id', help='Route id for displaying the bus details.')
args = parser.parse_args()

route_url = all_routes_url + "/" + args.route_id
soup = get_data_from_url(route_url, "routeDetailsHtml")
if soup:
	stop_details = soup.find_all("div", "col-xs-10 col-sm-10 col-md-10 resized bordered")
	print "\nStop details for " + args.route_id + ":\n"
	for i in range(len(stop_details)):
		print stop_details[i].text
else:
	print "\nBus service not available on entered route id. :(\n"
			
