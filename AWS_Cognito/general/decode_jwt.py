import json, time, os, urllib.request
from jose import jwk, jwt
from decouple import config
from jose.utils import base64url_decode

region = config('COGNITO_REGION_NAME')
userpool_id = config('USER_POOL_ID')
app_client_id = config('CLIENT_ID')

keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

with urllib.request.urlopen(keys_url) as f:
    response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']

def lambda_handler(token, context):
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False

    public_key = jwk.construct(keys[key_index])

    message, encoded_signature = str(token).rsplit('.', 1)

    decoded_signature = base64url_decode(encoded_signature.encode('urf-8'))

    if not public_key.verify(message.encode('urf-8'), decoded_signature):
        print('SIGNATURE veridication - FAILED')
        return False

    print('SIGNATURE SUCCESSFULLY - VERIFIED')

    claims = jwt.get_unverified_claims(token)

    if time.time() > claims['exp']:
        print('[!] Token is expired')
        return False

    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False

    return claims

if __name__ == '__main__':
    event = {'id_token': ''}
    lambda_handler(event, None)