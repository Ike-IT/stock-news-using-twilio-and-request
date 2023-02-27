import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = YOUR API_KEY
NEWS_API_KEY = YOUR API_KEY
TWILIO_SID = YOUR SID
TWILIO_AUTH_TOKEN = YOUR AUTH_TOKEN

stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY
    }
response = requests.get(STOCK_ENDPOINT, params=stock_params)
# print(response.status_code)
response.raise_for_status()
data = (response.json())["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]  #This dictionary comprehension turns a JSON file to a list.
yesterday_data = data_list[0]
# print(yesterday_data)
yesterdays_closing_price = yesterday_data["4. close"]
# print(yesterdays_closing_price)


day_before_yesterday_data = data_list[1]
# print(day_before_yesterday)
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
# print(day_before_yesterday_closing_price)


closing_price_difference = float(yesterdays_closing_price) - float(day_before_yesterday_closing_price)
# print(closing_price_difference)
up_down = None
if closing_price_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percent = round(closing_price_difference / float(yesterdays_closing_price) * 100)
# print(diff_percent)
if abs(diff_percent) > 0.7:
    news_param = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_param)
    articles = news_response.json()["articles"]
    # print(articles)

    three_articles = articles[:3]
    # print(three_articles)

    formatted_articles_list = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief:{article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles_list:
        message = client.messages.create(
            body=article,
            from_="+16693222517",
            to="+393479651447"
        )



