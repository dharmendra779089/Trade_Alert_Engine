# Import the requests library to make HTTP requests to the Alpha Vantage and News APIs
import requests
# Import the Client class from the twilio library to authorize and send SMS messages
from twilio.rest import Client

# Define your virtual phone number provided by Twilio (the sender)
VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
# Define your actual personal phone number verified on your Twilio account (the recipient)
VERIFIED_NUMBER = "your own phone number verified with Twilio"

# Set the stock ticker symbol for the company you are tracking
STOCK_NAME = "TSLA"
# Set the full company name to use when searching for relevant news articles
COMPANY_NAME = "Tesla Inc"

# Define the Alpha Vantage API endpoint URL for stock data
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
# Define the News API endpoint URL for fetching articles
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Store your personal Alpha Vantage API key
STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
# Store your personal News API key
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"
# Store your Twilio account SID for authentication
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
# Store your Twilio authentication token
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

## STEP 1: Get yesterday's closing stock price and the day before yesterday's closing stock price

# Create a dictionary of parameters to send with the Alpha Vantage API request
stock_params = {
    "function": "TIME_SERIES_DAILY", # Request daily time series data
    "symbol": STOCK_NAME,            # Specify the stock ticker symbol (TSLA)
    "apikey": STOCK_API_KEY,         # Provide the API key for authentication
}

# Make a GET request to the Alpha Vantage API using the defined parameters
response = requests.get(STOCK_ENDPOINT, params=stock_params)
# Parse the JSON response and extract the "Time Series (Daily)" dictionary
data = response.json()["Time Series (Daily)"]
# Convert the dictionary values into a list to easily access data by index (e.g., [0] for yesterday, [1] for the day before)
data_list = [value for (key, value) in data.items()]

# Access the first item in the list, which contains yesterday's stock data
yesterday_data = data_list[0]
# Extract yesterday's closing price using the specific key "4. close"
yesterday_closing_price = yesterday_data["4. close"]
# Print yesterday's closing price to the console for debugging
print(yesterday_closing_price)

# Access the second item in the list, which contains the day before yesterday's stock data
day_before_yesterday_data = data_list[1]
# Extract the day before yesterday's closing price
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
# Print the day before yesterday's closing price to the console
print(day_before_yesterday_closing_price)

# Calculate the raw difference between yesterday's and the day before yesterday's closing prices
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

# Initialize a variable to hold the directional emoji
up_down = None
# Check if the difference is positive (price went up)
if difference > 0:
    up_down = "🔺" # Assign an up-arrow emoji
# If the difference is negative (price went down)
else:
    up_down = "🔻" # Assign a down-arrow emoji

# Calculate the percentage difference relative to yesterday's closing price and round it to a whole number
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
# Print the percentage difference to the console
print(diff_percent)


## STEP 2: Use the News API to get articles related to the COMPANY_NAME if the stock fluctuates.

# Check if the absolute value of the percentage difference is greater than 1% (adjust to 5% if following original instructions exactly)
if abs(diff_percent) > 1:
    # Create a dictionary of parameters to send with the News API request
    news_params = {
        "apiKey": NEWS_API_KEY,      # Provide the API key for authentication
        "qInTitle": COMPANY_NAME,    # Search for the company name specifically in the article titles
    }

    # Make a GET request to the News API using the defined parameters
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    # Parse the JSON response and extract the list of articles
    articles = news_response.json()["articles"]

    # Use Python's slice operator to grab only the first 3 articles from the list
    three_articles = articles[:3]
    # Print the list of the 3 articles to the console for debugging
    print(three_articles)

    ## STEP 3: Use Twilio to send a separate message with each article's title and description.

    # Use a list comprehension to format each of the 3 articles into a clean string layout for SMS
    formatted_articles = [f"{STOCK_NAME}: {up_down}{abs(diff_percent)}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    # Print the formatted strings to the console
    print(formatted_articles)
    
    # Initialize the Twilio client using your account SID and auth token
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Iterate through the list of formatted article strings
    for article in formatted_articles:
        # Create and send an SMS message for the current article
        message = client.messages.create(
            body=article,                 # Set the message body to the formatted article string
            from_=VIRTUAL_TWILIO_NUMBER,  # Set the sender number to your virtual Twilio number
            to=VERIFIED_NUMBER            # Set the recipient number to your verified personal number
        )