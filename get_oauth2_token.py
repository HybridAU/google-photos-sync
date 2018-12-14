"""
This script will attempt to open your webbrowser,
perform OAuth 2 authentication and print your access token.

It depends on the library oauth2client which is depreciated.

This script was copied from https://github.com/burnash/gspread/wiki/How-to-get-OAuth-access-token-in-console%3F

If I ever want to get this to a point where others can use it
I'm going to have to make this a seemless process, maybe look at using
oauthlib to get the token and saving it into a database.
"""

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow
from oauth2client.file import Storage

import settings

flow = OAuth2WebServerFlow(
    client_id=settings.OAUTH_2_CLIENT_ID,
    client_secret=settings.OAUTH_2_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/photoslibrary',
    redirect_uri='http://example.com/auth_return')

storage = Storage('creds.data')

credentials = run_flow(flow, storage)

print("access_token: %s" % credentials.access_token)
