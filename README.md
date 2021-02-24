# @newspaper_snippets

A bot that posts snippets of newspapers from 100 years ago! Check it out on Instagram at [@newspaper_snippets](https://instagram.com/newspaper_snippets) and on Twitter at [@news_snippets](https://twitter.com/news_snippets)!

![instagram](./images/instagram.png)

## A Little Overview

So, recently, I built a bot that posts snippets of newspapers from exactly 100 years ago. Hence the name: newspaper_snippets! Here's what its jobs are:

-   Downloads a newspaper from Chronicling America

-   Finds a good focal point (though not all of them are the greatest)

-   Crops the image with a size of 1024 by 1024 (Max 1:1 size for Instagram)

-   Posts it on Instagram at [@newspaper_snippets](https://instagram.com/newspaper_snippets) and on Twitter at [@news_snippets](https://twitter.com/news_snippets)



## ONCE AGAIN, CHECK IT OUT HERE!

Check it out on Instagram at [@newspaper_snippets](https://instagram.com/newspaper_snippets) and on Twitter at [@news_snippets](https://twitter.com/news_snippets)!



## The Why?

I always wanted to create some form of art bot, but could never think of anything that would be interesting and different. This isn't that different either, but it was fun. It was created in a day, so the code is messy and needs fixing. Over time, I plan to tweak it and add more features, and especially clean up everything.

## What I Want to Add

-   Better focal point detections (Such as prioritizing better images)

-   Better Instagram integration. I couldn't find any working python libraries, so I may make my own.

-   Gain more followers. But that's not too important.

## Running it on Your Own

To install newspaper_snippets and run it on your own accounts, first clone it then install dependencies.

```bash
git clone https://github.com/zackumar/newspaper_snippets.git
pip install -r requirements.txt
```

Then add your credentials to `ns_config.py`

```python
instagram = {
    "username": "YOUR USERNAME",
    "password": "YOUR PASSWORD"
}

twitter = {
    "consumer_key": "KEY",
    "consumer_secret": "SECRET",
    "access_token_key": "KEY",
    "access_token_secret": "SECRET"
}
```

For Instagram, all you need is an account's username and password, but for Twitter, you need to add an app to your account to get access to your tokens.

After you should be able to run newspaper_snippets using:

```bash
python newspaper_snippets.py
```

## Also!

Check out [Chronicling America from the Library of Congress](https://chroniclingamerica.loc.gov/) where all of these images are from. It's pretty cool. They have a ton of newspapers from the U.S. I'm using the ones from 1777 to 1963 and there are a lot of editions. It's real neat.
