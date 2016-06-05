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
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.

    search_response = youtube.search().list(
        q=search_term,
        type="video",
        part="id,snippet",
        maxResults=1
    ).execute()

    vid_id = search_response.get("items", [])[0]["id"]["videoId"]
    statistics_response = youtube.videos().list(
        part="id,statistics",
        id=vid_id
    ).execute()

    result = dict()

    result["youtube_id"] = vid_id
    result["title"] = search_response.get("items", [])[0]["snippet"]["title"]
    #result["category_id"] = search_response.get("items", [])[0]["snippet"]["categoryId"]
    result["view_count"] = statistics_response.get("items", [])[0]["statistics"]["viewCount"]
    result["likes"] = statistics_response.get("items", [])[0]["statistics"]["likeCount"]

    return result

if __name__ == '__main__':
    youtube_search("avatar trailer")