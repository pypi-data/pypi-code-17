from pyvdp.paai.dispatcher import VisaPaaiDispatcher


def send(data):
    """Submits General Card Attributes Inquiry request.

    :param GeneralInquiryModel data: **Required**. 
        Instance of :func:`~pyvdp.paai.generalattinq.cardattributes.GeneralInquiryModel`
    :return: Dictionary with VDP response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.paai.geeneralattinq.cardattributes import generalinquiry, GeneralInquiryModel
        
        data_kwargs = {
            "primaryAccountNumber": "4957030420210512",
        }
        
        data = GeneralInquiryModel(**data_kwargs)
        result = generalinquiry.send(data)
        print(result)    
    """
    c = VisaPaaiDispatcher(resource='paai',
                           api='generalattinq',
                           method='cardattributes/generalinquiry',
                           http_verb='POST',
                           data=data)
    return c.send()
