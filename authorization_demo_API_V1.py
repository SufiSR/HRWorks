import requests
import datetime
import hashlib
from hashlib import sha256
import hmac


def Formatting_to_HRWorks_Date(date):
    date = str(date.replace(microsecond=0).isoformat()).replace("-", "").replace(":", "") + "Z"
    return date

def create_request_headers(target, payload, credentials):
    # First we need todays date in the HRWorks Format
    today = Formatting_to_HRWorks_Date(datetime.datetime.today())
    # Creating the canonical request
    canonical = "POST" + "\n" + \
                "/" + "\n\n" + \
                "content-type:application/json" + "\n" + \
                "host:"+credentials['url']+"\n" + \
                "x-hrworks-date:" + today + "\n" + \
                'x-hrworks-target:' + target + "\n" + "\n"
    canonical_plus_hash = canonical + sha256(str(payload).encode('utf-8')).hexdigest()
    # Creating the string to sign
    signature_string = 'HRWORKS-HMAC-SHA256\n' + today + '\n' + sha256(canonical_plus_hash.encode('utf8')).hexdigest()
    # Creating the signature value
    signed = hmac.new(
        key=hmac.new(
            key=hmac.new(
                key=hmac.new(
                    key=bytes("HRWORKS" + credentials['accessSecretKey'], 'utf8'),
                    msg=bytes(today[:today.find("T")], 'utf8'),
                    digestmod=hashlib.sha256).digest(),
                msg=bytes("production", 'utf8'),
                digestmod=hashlib.sha256).digest(),
            msg=bytes("hrworks_api_request", 'utf8'),
            digestmod=hashlib.sha256).digest(),
        msg=bytes(signature_string, 'utf8'),
        digestmod=hashlib.sha256).hexdigest()
    # Creating the authorization header
    authorization_header = {
        'Host': "api.hrworks.de",
        'Date': today,
        'x-hrworks-date': today,
        'Authorization': 'HRWORKS-HMAC-SHA256 Credential=' + credentials['accessKey'] + "/production, SignedHeaders=content-type;host;x-hrworks-date;x-hrworks-target, Signature=" + signed,
        'Content-Type': 'application/json',
        'x-hrworks-target': target
    }
    return authorization_header

## ENTER YOUR CREDENTIALS HERE ## 
server_credentials = {
    'accessKey': 'YOUR_ACCESS_KEY',
    'accessSecretKey': 'YOUR_ACCESS_SECRET',
    'url': 'api.hrworks.de'
}
## ENTER YOUR CREDENTIALS HERE ## 

target = 'GetPresentPersonsOfOrganizationUnit'  # e.g. 'GetAllActivePersons'
payload = '{"organizationUnitNumber": "1"}'  # e.g. ''

headers = create_request_headers(target, payload, server_credentials)
r = requests.post('https://api.hrworks.de', headers=headers, data=payload)
print(r.json())
