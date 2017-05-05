import tweepy
import yaml
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def report_spam(spam_screen_name):
    """Report spam by all the account."""
    for sn in get_screen_names():
        api = get_api(sn)
        print(sn, end=' / ')
        try:
            api.report_spam(screen_name=spam_screen_name)
            print('success')
        except:
            print('fail')

def get_screen_names():
    """Return all the screen_names registerd."""
    creds = get_creds()
    return list(creds.keys())

def get_creds():
    """Get credentials."""
    path = os.path.join(__location__, 'credentials.yaml')
    with open(path) as f:
        creds = yaml.load(f)
    return creds

def write_creds(creds):
    """Write credentials."""
    path = os.path.join(__location__, 'credentials.yaml')
    with open(path, 'w') as f:
            yaml.dump(creds, f)

def get_api(username='sakuramochi_0'):
    '''TweepyのREST APIオブジェクトを作る'''

    # get credentials
    credentials = get_creds()
    while username not in credentials:
        # add a new user dictionary
        if input('Create new user? [y/N] ') == 'y':
            # if new user, set app_key & app_secret
            app_key = input('Input app_key: ')
            app_secret = input('Input app_secret: ')
            credentials[username] = {
                'app_key': app_key,
                'app_secret': app_secret,
            }
        else:
            print('User list:')
            for i, name in enumerate(credentials.keys()):
                print('  *', name)
            username = input('Which user do you use? ')
    credential = credentials.get(username, None)
    
    if 'oauth_token' not in credential:
        # authentication first step
        auth = tweepy.OAuthHandler(consumer_key=credentials[username]['app_key'],
                                   consumer_secret=credentials[username]['app_secret'])
        print(auth.get_authorization_url())
        pin = input('Enter PIN code: ')

        # final step
        credential['oauth_token'], credential['oauth_token_secret'] = auth.get_access_token(pin)
        credentials[username] = credential

        write_creds(credentials)
    else:
        auth = tweepy.OAuthHandler(consumer_key=credentials[username]['app_key'],
                                   consumer_secret=credentials[username]['app_secret'])
        auth.set_access_token(credentials[username]['oauth_token'],
                              credentials[username]['oauth_token_secret'])
        auth.username = username

    return tweepy.API(auth)

