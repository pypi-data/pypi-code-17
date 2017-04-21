from pyvdp.paai.dispatcher import VisaPaaiDispatcher


def send(data):
    """Submits Funds Transfer Inquiry request.

    :param FundsTransferInquiryModel data: **Required**. 
        Instance of :func:`~pyvdp.paai.fundstransferattinq.cardattributes.FundsTransferInquiryModel`
    :return: Dictionary with VDP response.
    
    **Usage:**
    
    ..  code:: python
    
        from pyvdp.paai.fundstransferattinq.cardattributes import fundstransferinquiry, FundsTransferInquiryModel
        
        data_kwargs = {
            "primaryAccountNumber": "4957030420210512",
        }
        
        data = FundsTransferInquiryModel(**data_kwargs)
        result = fundstransferinquiry.send(data)
        print(result)
    """
    c = VisaPaaiDispatcher(resource='paai',
                           api='fundstransferattinq',
                           method='cardattributes/fundstransferinquiry',
                           http_verb='POST',
                           data=data)
    return c.send()
