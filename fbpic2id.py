#!/usr/bin/python
# fbpic2id.py
# Author: stderr (www.chokepoint.net)
# Given a direct link to a Facebook image, return the owner's name & URL (if available)
# 	Also return anyone tagged in the photo along with their profile (if available)
#	If the owner returns as Facebook, privacy settings don't allow a non logged in user to view the content
#	For better results implement logging in to a FB profile

import sys
from BeautifulSoup import BeautifulSoup
import requests

def main(argv):
	if len(argv) != 1:
		print "Usage: ./fbpic2id.py <Facebook Image URL>"
		exit(1)
	
	pic_url = argv[0]
	album_url = "http://www.facebook.com/photo.php?fbid=" + pic_url.split('_')[1]
	headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; nl; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13'}

	print "\nAlbum URL: " + album_url + "\n"
	
	req = requests.get(album_url, headers=headers)
	soup = BeautifulSoup(req.text)
	
	# Grab the name of the owner that posted it. 
	# if the title isn't "Timeline Photos | Facebook" it must be a user
	divTag = soup.findAll('title')
	if divTag[0].text != "Timeline Photos | Facebook": 
		if divTag[0].text.split('&')[0] == "Facebook":
			print "Can't find owner due to privacy settings"
			exit(1)
		print "Owner: " + divTag[0].text.split('&')[0] 
	else:
		divTag = soup.findAll('a')
		for tag in divTag:
			if tag.text.find("&#039;s Photos") != -1:
				print "Owner (Page/Group): " + tag.text.split('&')[0]
	
	# If privacy settings are open, grab the link to the owner's page
	divTag = soup.findAll('div', {'id':'fbPhotoPageAuthorPic'})
	for tag in divTag:
		aTags = tag.findAll('a')
		for tag in aTags:
			if tag['href'] != '#':
				print "Owner URL: "+tag['href']
			else:
				print "Owner's URL Blocked by privacy settings"
	# Grab all people tagged with weak privacy settings
	divTag = soup.findAll('a', {'class':'taggee'})
	print "\nTagged with profiles:"
	for tag in divTag:
		print tag.text + " (" + tag['href'] + ")"
	
	# Grab the rest of the tagged people's names
	print "\nTagged without profiles:"
	divTag = soup.findAll('span', {'class':'taggee'})
	for tag in divTag:
		print tag.text
	
if __name__ == "__main__":
	main(sys.argv[1:])
