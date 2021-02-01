from app import app, api, bom
from flask import render_template, request, flash, session
import json
import tweepy as tw

base_url = "https://twitter.com/"

@app.route("/", methods=["GET", "POST"])
def index():
    
    trends_lists = []
    country = ""

    if request.method == "POST":
        noRt = request.form.get("noRt")
        noLink = request.form.get("noLink")
        country = request.form.get("country")

        trends = api.trends_available()
        for trend in trends:
            if trend["countryCode"] == country and trend["placeType"]["name"] == "Country":
                trend_country = trend
                trends_lists = api.trends_place(trend_country["woeid"])
                break

        
    
    return render_template("index.html", trends=trends_lists, country=country)


@app.route("/users", methods=["POST", "GET"])
def users():

    if request.method == "POST":
        search_term = request.form.get("trending")
        tweets = tw.Cursor(api.search, q=search_term, tweet_mode="extended").items(100)
        users = [ tweet.user.screen_name for tweet in tweets]

        list_count = []
        temp = {}
        n = 0

        users_set = set(users)

        while n < len(users_set):
            for user in users:
                temp["username"] = user
                temp["count"] = users.count(user)
                temp["url"] = base_url + user
                users = [ item for item in users if item != user ]
                n += 1
                list_count.append(temp.copy())
                break
        
        list_count.sort(reverse=True, key=lambda item: item["count"])

    return render_template("hot-user.html", list_count=list_count, trend=search_term)

@app.route("/checker/<user>", methods=["POST", "GET"])
def checker(user):
    if request.method == "GET":
        result = bom.check_account(user)

        user_data = api.get_user(user)

        profile_url = base_url + user

        botometer = round(float(result["cap"]["universal"]*100), 2)
        
    return render_template("checker.html", user=user_data, botometer=botometer, url=profile_url)