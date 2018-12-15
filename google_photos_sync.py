"""
Sync Google Photos with local storage
"""
import json

import google.oauth2.credentials
import google.auth.transport.requests

import settings

credentials = google.oauth2.credentials.Credentials(
    settings.OAUTH_2_ACCESS_TOKEN,
    refresh_token=settings.OAUTH_2_REFRESH_TOKEN,
    token_uri=settings.OAUTH_2_TOKEN_URI,
    client_id=settings.OAUTH_2_CLIENT_ID,
    client_secret=settings.OAUTH_2_CLIENT_SECRET)

authed_session = google.auth.transport.requests.AuthorizedSession(credentials)


def download_latest_file():
    """
    Basicly Just test dummy code to download the latest photo.

    All we are doing here is donloading the latest file, it's pretty crude and
    it won't work if the latest media item is a video but it's baby steps
    towards something useful.
    """
    media_items = authed_session.get("https://photoslibrary.googleapis.com/v1/mediaItems")

    latest_media = json.loads(media_items.text)
    latest_photo_url = latest_media['mediaItems'][0]['baseUrl']
    latest_photo_width = latest_media['mediaItems'][0]['mediaMetadata']['width']
    latest_photo_file_name = latest_media['mediaItems'][0]['filename']

    # We don't actually have to use an authenticated session here, we could just
    # use the standard requests library to pull it down.
    photo = authed_session.get(latest_photo_url + "=w" + latest_photo_width)

    file = open(latest_photo_file_name, 'wb')
    file.write(photo.content)
    file.close()


def upload_test_photo():
    """
    Again, just dummy test code for now uploads a file called test_image.jpg

    It looks like uploading an image happens in two parts, first you upload
    the image and that gives you an upload token, then you create the image
    by posting the token (and presumably any album if you want to add it to
    a specific one.)
    """
    test_photo = open('test_image.jpg', 'rb')

    upload_headers = {
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': 'test_image.jpg',
        'X-Goog-Upload-Protocol': 'raw'}

    upload_result = authed_session.post(
        "https://photoslibrary.googleapis.com/v1/uploads",
        headers=upload_headers,
        data=test_photo.read())

    create_headers = {'Content-type': 'application/json'}
    create_data = {
        "newMediaItems": [{
            "description": "Uploaded by API",
            "simpleMediaItem":{
                "uploadToken": upload_result.text
                }
            }]
        }

    create_result = authed_session.post(
        "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate",
        headers=headers,
        data=json.dumps(create_data))

    print(create_result, create_result.text)
