import tweepy
import ns_config


def postTwitter(filename, caption):
    auth = tweepy.OAuthHandler(
        ns_config.twitter["consumer_key"], ns_config.twitter["consumer_secret"])
    auth.set_access_token(
        ns_config.twitter["access_token_key"], ns_config.twitter["access_token_secret"])
    api = tweepy.API(auth)

    api.update_with_media(filename, caption)
