from instabot import Bot


def postInstagram(instagram, filename, caption):
    bot = Bot()
    bot.login(username=username, password=password)
    bot.upload_photo('./profilepic.jpg', caption='TEST')
