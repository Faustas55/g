import pytest
from polonius_api import send_data,get_token,get_casePayload


caseUrl = "https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProduct"
infringUrl = "https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProductInf"
tokenurl="https://syngenta.poloniouslive.com/syngentatraining/pcmsrest/oauth/token?"



@pytest.mark.parametrize("row",[
    {'region': 'China', 'country': 'Hong Kong', 'business': 'Crop Protection', 
    'OffenceType': 'Online Counterfeit','category':'takedown','date_found':'20-04-2030',
    'seller':'meeeeee','product':'crap and more crap ','url':'www.syngenta.com////sfjsdf!1232$'
    }
    
])

def test_get_payload(row):
    test=get_casePayload(row)
    print(test)




@pytest.mark.parametrize("casePayload",[
    {'region': 'China', 'country': 'Hong Kong', 'businessUnit': 'Crop Protection', 'OffenceType': 'Online Counterfeit', 'incidentDescription': 'HADES UPLOAD: \n suspected counterfeiter \n date found : 24-02-2020 \n Product Title: Syngenta Velista Fungicide WSG 22 oz NEW \n Seller Name: 59scorpion88 \n\n url: https://www.ebay.com.hk/itm/Syngenta-Velista-Fungicide-WSG-22-oz-NEW-/283788383164'},
    {'region': 'NA', 'country': 'Canada', 'businessUnit': 'Crop Protection', 'OffenceType': 'Online Counterfeit', 'incidentDescription': 'HADES UPLOAD: \n suspected counterfeiter \n date found : 24-02-2020 \n Product Title: Syngenta Velista Fungicide WSG 22 oz NEW \n Seller Name: 59scorpion88 \n\n url: https://www.ebay.com.hk/itm/Syngenta-Velista-Fungicide-WSG-22-oz-NEW-/283788383164'},
    {'region': 'LATAM', 'country': 'Peru', 'businessUnit': 'Crop Protection', 'OffenceType': 'Online Counterfeit', 'incidentDescription': 'HADES UPLOAD: \n suspected counterfeiter \n date found : 24-02-2020 \n Product Title: Syngenta Velista Fungicide WSG 22 oz NEW \n Seller Name: 59scorpion88 \n\n url: https://www.ebay.com.hk/itm/Syngenta-Velista-Fungicide-WSG-22-oz-NEW-/283788383164'},
     {'region': 'EAME', 'country': 'France', 'businessUnit': 'Crop Protection', 'OffenceType': 'Online Counterfeit', 'incidentDescription': 'HADES UPLOAD: \n suspected counterfeiter \n date found : 24-02-2020 \n Product Title: Syngenta Velista Fungicide WSG 22 oz NEW \n Seller Name: 59scorpion88 \n\n url: https://www.ebay.com.hk/itm/Syngenta-Velista-Fungicide-WSG-22-oz-NEW-/283788383164'},
     
])





def test_senddata(casePayload):
    
        headers=get_token(tokenurl)
        caseId=send_data(headers,caseUrl,casePayload=casePayload)
        assert caseId["responseText"]=='Created'



