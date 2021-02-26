# @newspaper_snippets

A bot that posts snippets of newspapers from 100 years ago! Check it out on Instagram at [@newspaper_snippets](https://instagram.com/newspaper_snippets) and on Twitter at [@news_snippets](https://twitter.com/news_snippets)!

![instagram](./images/instagram.png#center)

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

Just because I'm currently using a NodeJS module for Instagram, you'll need to also instal those dependencies.

```bash
npm install
```

For Instagram, all you need is an account's username and password, but for Twitter, you need to add an app to your account to get access to your tokens. You need to put those in your environment variables. You can use `pipenv` if you would like. 

```
instagram_username: <your username>
instagram_password: <your password>

twitter_consumer_key: <twitter consumer key>
twitter_consumer_secret: <twitter consumer secret>
twitter_access_token: <twitter access token>
twitter_access_token_secret: <twitter access token secret>
```

After you should be able to run newspaper_snippets using:

```bash
python ./src/newspaper_snippets.py
```

## Running it on heroku

You can also run this using heroku.

There are two ways to install it.
You can fork this repo and deploy using github integration in the Heroku web app. Or you can clone this repo and deploy it using the Heroku CLI. Either way, you will need to add the same environement variables as above in Heroku's config vars.

For Twitter, you will need to go to [developer.twitter.com](https://developer.twitter.com) and make and connect and app to your Twitter account. 

## Also!

Check out [Chronicling America from the Library of Congress](https://chroniclingamerica.loc.gov/) where all of these images are from. It's pretty cool. They have a ton of newspapers from the U.S. I'm using the ones from 1777 to 1963 and there are a lot of editions. It's real neat.

## Some Links!

-   [Instagram](https://instagram.com/newspaper_snippets)
-   [Twitter](https://twitter.com/news_snippets)
-   [Blog Post](https://zackumar.github.io/blog?title=@newspaper_snippets)
-   [linktr.ee](https://linktr.ee/news_snips)
