#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDUx-R__S3VcKDN54oCsBCatYQC_7WCl_U"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(search_term):
	# argparser.add_argument("--q", help="Search term", default="mostafa")
	# argparser.add_argument("--max-results", help="Max results", default=25)
	# args = argparser.parse_args()
	# args.q = search_term
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	                developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
			q=search_term,
			part="id,snippet",
			maxResults=1
	).execute()

	videos = []
	channels = []
	playlists = []


	vid_id = search_response.get("items", [])[0]["id"]["videoId"]
	statistics_response = youtube.videos().list(
			part="id,statistics",
			id = vid_id
	).execute()


	result = {}

	result["youtube_id"] = vid_id
	result["title"] = search_response.get("items", [])[0]["snippet"]["title"]
	#result["category_id"] = search_response.get("items", [])[0]["snippet"]["categoryId"]
	result["view_count"] = statistics_response.get("items", [])[0]["statistics"]["viewCount"]
	result["likes"] = statistics_response.get("items", [])[0]["statistics"]["likeCount"]

	#print result
	return result

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	#print search_response.get("items", [])[0]
	#print statistics_response.get("items", [])[0]
	# for search_result in search_response.get("items", []):
	# 	if search_result["id"]["kind"] == "youtube#video":
	# 		videos.append("%s (%s)" % (search_result["snippet"]["title"],
	# 		                           search_result["id"]["videoId"]))
	# 	elif search_result["id"]["kind"] == "youtube#channel":
	# 		channels.append("%s (%s)" % (search_result["snippet"]["title"],
	# 		                             search_result["id"]["channelId"]))
	# 	elif search_result["id"]["kind"] == "youtube#playlist":
	# 		playlists.append("%s (%s)" % (search_result["snippet"]["title"],
	# 		                              search_result["id"]["playlistId"]))

	#print "Videos:\n", "\n".join(videos), "\n"
	#print "Channels:\n", "\n".join(channels), "\n"
	#print "Playlists:\n", "\n".join(playlists), "\n"


#if __name__ == '__main__':
#	youtube_search("1001 Inventions and the World of Ibn Al-Haytham")
