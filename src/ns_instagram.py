from instagrapi import Client


def postInstagram(instagram, filename, caption):
    cl = Client()
    print('Logging in...')
    try:
        cl.login(username=instagram['username'],
                 password=instagram['password'])
    except:
        print('Hit error but continuing')

    print('Uploading...')
    cl.photo_upload(filename, caption)
