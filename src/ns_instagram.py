from instagrapi import Client


def postInstagram(instagram, filename, caption):
    cl = Client()
    print('Logging in...')
    cl.login(username=instagram['username'], password=instagram['password'])
    print('Uploading...')
    cl.photo_upload(filename, caption)
