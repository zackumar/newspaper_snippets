import tweepy


def postTwitter(twitter, filename, caption, disclaimer=False):
    auth = tweepy.OAuthHandler(
        twitter["consumer_key"], twitter["consumer_secret"])
    auth.set_access_token(
        twitter["access_token_key"], twitter["access_token_secret"])
    api = tweepy.API(auth)

    if (disclaimer):
        disclaimer_img = api.media_upload('./images/disclaimer_lang.png')

    post = api.media_upload(filename)

    api.update_status(caption, media_ids=[
                      disclaimer_img.media_id, post.media_id])
