import time
from requests_oauthlib import OAuth1Session
import json
env = {
    "consumer_key": "<consumer_key>",
    "consumer_secret": "<consumer_secret>",
    "access_token": "<access_token>",
    "access_token_secret": "<access_token_secret>",
    "bearer_token": "<bearer_token>"
}

# Authenticate to Twitter
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(env["consumer_key"], client_secret=env["consumer_secret"])
try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    env["consumer_key"],
    client_secret=env["consumer_secret"],
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    env["consumer_key"],
    client_secret=env["consumer_secret"],
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def deleteTweet():
    response = oauth.delete("https://api.twitter.com/2/tweets/1440778129307461632")

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response status: {}".format(response.status_code))

    print("Data: {}".format(response.json()))

while True: # Loop forever, errors are ignored.
    try:
        deleteTweet()
    except:
        pass
    time.sleep(60)