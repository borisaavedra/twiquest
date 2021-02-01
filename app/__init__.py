from flask import Flask
import tweepy as tw
import botometer
import os


consumer_key = os.environ.get("COSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
rapidapi_key = os.environ.get("RAPIDAPI_KEY")


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

bom = botometer.Botometer(wait_on_rate_limit=True,
                            rapidapi_key=rapidapi_key,
                            consumer_key=consumer_key,
                            consumer_secret=consumer_secret,
                            access_token=access_token,
                            access_token_secret=access_token_secret)


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True)


from app import routes

