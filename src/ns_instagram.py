from instabot import Bot


def postInstagram(instagram, filename, caption):
    bot = Bot()
    bot.login(username=instagram['username'], password=instagram['password'])
    bot.upload_photo(filename, caption='TEST')
