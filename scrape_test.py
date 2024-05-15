from twikit import Client

USERNAME = 'YOUR TWITTER @'
EMAIL = 'YOUR TWITTER EMAIL'
PASSWORD = 'YOUR ACCOUNT PASSWORD'

# Initialize client
client = Client(language='en-US')

client.login(
    auth_info_1=USERNAME,
    auth_info_2=EMAIL,
    password=PASSWORD
)

term = 'python'

tweets = client.search_tweet(f'{term} lang:en', 'Latest')
print(len(tweets))
for tweet in tweets:
    '''print(
        tweet.user.name,
        tweet.text,
        tweet.created_at
    )'''
    print(tweet.text)