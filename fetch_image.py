import os
from bs4 import BeautifulSoup
import json
import urllib.request
import urllib.parse
import shutil

DIR = "_browserCache_"


def get_soup(url, header):
    # return complete page html code
    return BeautifulSoup(
        urllib.request.urlopen(urllib.request.Request(url, headers=header)),
        "html.parser",
    )


def bing_image_search(query, callback, size):
    query = query.split()
    query = "+".join(query)
    # &FORM=HDRSC2 for save image as
    url = "http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    header = {"User-Agent": "Chrome/43.0.2357.134"}
    soup = get_soup(url, header)
    ActualImages = []  # contains the link for Large original images, type of  image

    for a in soup.find_all("a", {"class": "iusc"})[:size]:
        m = json.loads(a["m"])
        turl = m["turl"]  # desktop images url
        murl = m["murl"]  # mobile images url

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        ActualImages.append((image_name, turl, murl))

    cache_image(ActualImages, callback)


def cache_image(ActualImages, callback):
    if os.path.exists(DIR) == True:
        shutil.rmtree(DIR)

    if os.path.exists(DIR) == False:
        os.mkdir(DIR)
    count = 0
    for item in ActualImages:
        image_name, turl, murl = item
        try:
            file_name = image_name.split(".")[0] + ".jpg"
            urllib.request.urlretrieve(turl, "%s/" % (DIR) + file_name)
            count = count + 1
            callback((file_name, count))

        except Exception as e:
            print("could not load : " + image_name)
            print(e)

            # raw_img = urllib.request.urlopen(turl).read()
            # f = open(os.path.join(DIR, image_name), 'wb')
            # f.write(raw_img)
            # f.close()


# bing_image_search('ratan ghosley')
# def downloadImage(query, n=4):
# 	query = query.replace('images','')
# 	query = query.replace('image','')
# 	query = query.replace('search','')
# 	query = query.replace('show','')
# 	URL = "https://www.google.com/search?tbm=isch&q=" + query
# 	result = requests.get(URL)
# 	src = result.content

# 	soup = BeautifulSoup(src, 'html.parser')
# 	imgTags = soup.find_all('img', class_='Q4LuWd')

# 	if os.path.exists('Downloads')==False:
# 		os.mkdir('Downloads')

# 	count=0
# 	for i in imgTags:
# 		if count==n: break
# 		try:
# 			urllib.request.urlretrieve(i['src'], 'Downloads/' + str(count) + '.jpg')
# 			count+=1
# 			print('Downloaded', count)
# 		except Exception as e:
# 			raise e

# downloadImage('ratan tata',9)
