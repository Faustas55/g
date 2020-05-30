# Import libraries
import requests


# Creates header for OAuth request
url='https://syngenta.poloniouslive.com/syngentatraining/pcmsrest/oauth/token?'
payload={'client_secret':'TbKs0R3e@A6V!p6c^Wq6CdPc','client_id':'publicRestCall', 'grant_type':'client_credentials'}


# request a token for access 
r=requests.post(url,data=payload)
response=r.json()
print(response['access_token'])

caseUrl='https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProduct'
headers={'Authorization':'Bearer '+ str(response['access_token']),'Content-Type':'text/plain'}
print(headers)

#country has to have a capital 
casePayload={

    "region": "EAME",
    "country": "Germany",
    "businessUnit": "Seeds",
    "OffenceType": "Online Counterfeit",
    "incidentDescription": "Hades Upload Found: 20/11/2020 | site: ebay.com|  Product Title: crap advion  | Seller Name: Daves chems | url: https://www.w3schools.com/css/default.asp"
    }



try :
    r=requests.post(url=caseUrl,headers=headers,json=casePayload)

except:
    print("There has been a problem uploading case data")

if r.json()['taskId']=="0":
    
    print("case was not added please check the payload. Make sure data is correct e.g Country has a capital")
else:
    print(r.text)