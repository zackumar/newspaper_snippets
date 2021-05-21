from instagrapi import Client


def postInstagram(instagram, filename, caption):
    cl = Client()
    cl.login(username=instagram['username'], password=instagram['password'])
    cl.photo_upload(filename, caption)
