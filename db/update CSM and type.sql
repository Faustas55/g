UPDATE advert
SET SP_lastname = (Select SP_lastname from CSM where advert.country=csm.country),
SP_firstname = (Select SP_firstname from CSM where advert.country=csm.country),
type='Distributor'




