import tweepy
import configparser
import json

from django.shortcuts import render
from django.views import View




class IndexView(View):
    def get(self, request):

        return render(request, 'parsing/index.html')

    def post(self, request):

        accounts = request.POST.get('accounts').strip()
        accounts = [account.strip().split('/')[-1] for account in accounts.split('\n')]


        config = configparser.ConfigParser()
        config.read('twitterparser/config.ini')

        api_key = config['twitter']['api_key']
        api_secret_key = config['twitter']['api_secret_key']
        # api_bearer_token = config['twitter']['api_bearer_token']
        api_access_token = config['twitter']['api_access_token']
        api_access_token_secret = config['twitter']['api_access_token_secret']

        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(api_access_token, api_access_token_secret)

        api = tweepy.API(auth)
        
        users = []
        for account in accounts:
            id = account
            user = api.get_user(screen_name=id)
            user_id = user.id
            last_tweets = [tweet.text for tweet in api.user_timeline(user_id=user_id, count = 3)]
            user_info = {
                'followers': user.followers_count,
                'screen_name': user.name,
                'description': user.description,
                'friends': user.friends_count,
                'last_tweets': last_tweets,
            }
            
            users.append(user_info)

            # context.append({'user_info': user_info, 'last_tweets': last_tweets})
        context = {
            'users': users,
        }
        print(context)
        return render(request, 'parsing/index.html', context=context)