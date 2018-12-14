"""
Sync Google Photos with local storage
"""

import google.oauth2.credentials
import google.auth.transport.requests

import settings

credentials = google.oauth2.credentials.Credentials(
    settings.OAUTH_2_ACCESS_TOKEN)

authed_session = google.auth.transport.requests.AuthorizedSession(credentials)
media_items = authed_session.get('https://photoslibrary.googleapis.com/v1/mediaItems')

print(media_items.text)
