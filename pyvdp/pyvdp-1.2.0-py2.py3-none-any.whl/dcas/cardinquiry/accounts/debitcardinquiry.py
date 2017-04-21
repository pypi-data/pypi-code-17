from pyvdp.dcas.dispatcher import VisaDcasDispatcher


def send(data):
    """Submits DCAS Debit Card Inquiry request.
    
    :param DebitCardInquiryModel data: **Required**.
        Instance of :func:`~pyvdp.dcas.cardinquiry.accounts.DebitCardInquiryModel`. 
    :return: Response from VDP.
     
    **Usage**: 
    
    ..  code:: python
    
            from pyvdp.dcas.cardinquiry.accounts import debitcardinquiry, DebitCardInquiryModel
    
            cn_kwargs = {
                'first_name': 'John',
                'last_name': 'Doe'
            }
    
            data_kwargs = {
                'direct_dan': '0987654321',
                'routing_number': '1234567890',
                'cardholder_name': DebitCardInquiryModel.CardholderName(**cn_kwargs)
            }
    
            data = DebitCardInquiryModel(**data_kwargs)
            result = debitcardinquiry.send(data)
            print(result)     
    """
    c = VisaDcasDispatcher(api='cardinquiry',
                           method='accounts/debitcardinquiry',
                           http_verb='POST',
                           data=data)
    return c.send()
