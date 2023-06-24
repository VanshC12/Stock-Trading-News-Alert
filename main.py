import jovian
from twilio.rest import Client
jovian.commit(project="stock-trading-news-alert-project")
import requests

account_sid = 'AC2e69bb30a0511759b98d6e8ca383f3e4'
auth_token = '5b4c6f988dbe4fabfa9d26b7079cf797'
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY="C0QY0H0J6397K686"
NEWS_API_KEY="a2a81ca87cb349ecad980c59d2b5c0c1"
stock_params={
  "function":"TIME_SERIES_DAILY",
  "symbol":STOCK_NAME,
  "apikey":STOCK_API_KEY

}
response=requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

if diff_percent > 5:
    print("Get News")
if diff_percent > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)
three_articles = articles[:1]
print(three_articles)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=  'NASDAQ Symbol '+ STOCK_NAME +'\nCurrent Price = '+ yesterday_closing_price +'\nPrevious closing = '+
           day_before_yesterday_closing_price +'\nMargin ='+str(difference)+'\nPercentage Margin ='+str(diff_percent),
    to=   'whatsapp:+918291629854'
)

print(message.sid)