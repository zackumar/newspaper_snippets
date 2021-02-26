import tweepy


def postTwitter(twitter, filename, caption):
    auth = tweepy.OAuthHandler(
        twitter["consumer_key"], twitter["consumer_secret"])
    auth.set_access_token(
        twitter["access_token_key"], twitter["access_token_secret"])
    api = tweepy.API(auth)

    api.update_with_media(filename, caption)
