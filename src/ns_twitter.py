import tweepy


def postTwitter(twitter, filename, caption):
    auth = tweepy.OAuthHandler(
        twitter["consumer_key"], twitter["consumer_secret"])
    auth.set_access_token(
        twitter["access_token_key"], twitter["access_token_secret"])
    api = tweepy.API(auth)

    media = api.media_upload(filename)
    api.update_status(caption, media_ids=[media.media_id])
