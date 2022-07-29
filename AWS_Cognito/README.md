we create `.env` :"
```
REDIRECT_URI = 'http://localhost:8000/'
TOKEN_ENDPOINT = 'https://XXXXXX.auth.eu-central-1.amazoncognito.com/oauth2/token'

CLIENT_ID = '7bjXXXXXXXbqnt99v30vrrek8'
CLIENT_SECRET = '1XXXXXXX1o1v62ir326lvqo7giqf54ltnu2htjs9vkaegsg1l3u'
USER_POOL_ID = 'eu-central-1_XXXXXXXX'
COGNITO_REGION_NAME = 'eu-central-1'
```
install these :
```
pip install python-decouple
pip install requests
pip install python-jose
```
Links in the `templates/index.html` structure/example:

Sign In URL -
https://[DOMAIN].auth.[AWS-REGION].amazoncognito.com/login?response_type=code&client_id=[APP_CLIENT_ID]&redirect_uri=[CALLBACK_URL]
https://XXXXXXXX.auth.eu-central-1.amazoncognito.com/login?response_type=code&client_id=7bjajxxxxxyyyyynt99v3rrek8&redirect_uri=http://localhost:8000/

Sign Out URL -
https://[DOMAIN].auth.[AWS-REGION].amazoncognito.com/logout?client_id=[APP_CLIENT_ID]&logout_uri=[SIGN_OUT_URL]
https://XXXXXXXX.auth.eu-central-1.amazoncognito.com/logout?client_id=7bjajxxxxxyyyyynt99v3rrek8&logout_uri=http://localhost:8000/sign-out

TOKEN_ENDPOINT -
https://[DOMAIN].auth.[AWS-REGION].amazoncognito.com/oauth2/token