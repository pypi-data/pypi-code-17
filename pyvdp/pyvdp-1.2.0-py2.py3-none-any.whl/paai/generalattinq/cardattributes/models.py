class GeneralInquiryModel(object):
    """General Card Attributes Inquiry data object model.

    :param str primaryAccountNumber: **Required**. Primary account number (PAN). 13-19 characters string.

    **Request:**
    
    ..  code:: json

        {
            "primaryAccountNumber": "4465390000029077"
        }
        
    **Response:**
    
    ..  code:: json
    
        {
            "status": {
                "statusCode": "CDI000",
                "statusDescription": "Success"
            },
            "cardProductId": "K",
            "cardProductName": "Visa Corporate T&amp;E",
            "cardProductSubtypeCode": "ON",
            "cardProductSubtypeDescription": "Other Prepaid-Non Reloadable",
            "cardTypeCode": "H",
            "cardSubtypeCode": "R",
            "cardPlatformCode": "CO",
            "issuerName": "BANCO AGROMERCANTIL DE GUATEMALA S.A.",
            "bin": "481507",
            "countryCode": "332"
        }    
    """
    ATTRS = [
        'primaryAccountNumber'
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)
