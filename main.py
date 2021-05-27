STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

import requests
import credential

END_POINT_STOCK = "https://www.alphavantage.co/query"

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": credential.get_api_key("stocks"),
}

response = requests.get(END_POINT_STOCK,stock_param)
response.raise_for_status()
data = response.json()

Data_Daily = data['Time Series (Daily)']

count = 0
first_two_days_data = {}
diff = []
date = []
for key in Data_Daily:
    if count < 2:
        first_two_days_data[key] = Data_Daily[key]
        date.append(key)
        diff.append(Data_Daily[key]['4. close'])
        print(key, Data_Daily[key]['4. close'])
        count+=1
    else:
        break #break, since we are not intersted in any other days after 2 days

change = float(diff[0]) - float(diff[1])
print("Change: ", change)
print("Percent diff: ", change/float(diff[0])*100)

cur_date = date[0]

END_POINT_NEWS = "https://newsapi.org/v2/everything"
news_param = {
    "q": COMPANY_NAME,
    "from": cur_date,
    "sortBy": "popularity",
    "apikey": credential.get_api_key("news")
}

response = requests.get(END_POINT_NEWS, news_param)
response.raise_for_status()
data = response.json()

# print(data['articles'][:3])
top_3_articles = data['articles'][:3]

formatted_article = [f"Headline: {article['title']}. \n Brief: {article['description']}  \n" for article in top_3_articles]

for m in formatted_article:
    print(m)