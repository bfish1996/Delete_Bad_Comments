import tweepy
import openai

# Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# OpenAI API credentials
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Function to fetch comments
def fetch_comments(tweet_id):
    return api.get_status(tweet_id, tweet_mode='extended')._json['full_text']

# Function to analyze comment
def analyze_comment(comment):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the following comment for negativity:\n\n{comment}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

# Function to delete comment
def delete_comment(comment_id):
    api.destroy_status(comment_id)

# Continuous monitoring
while True:
    for tweet in tweepy.Cursor(api.user_timeline).items():
        comments = fetch_comments(tweet.id)
        for comment in comments:
            analysis = analyze_comment(comment['text'])
            if 'negative' in analysis.lower():
                delete_comment(comment['id'])
    time.sleep(60)  # Check every minute
