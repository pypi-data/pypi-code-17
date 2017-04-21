class EnrollmentsModel(object):
    """Visa Mobile Location Confirmation Enrollments data object model.
    
    :param str enrollmentMessageType: **Required**. Flag, indicating enrollment or deenrollment. Possible values are:
        *'enroll'*, *'deenroll'*. 8 characters string.
    :param EnrollmentRequest enrollmentRequest: **Required**. 
        Instance of :func:`~pyvdp.mlc.enrollment.EnrollmentsModel.EnrollmentRequest`.
        
    **Request:**
    
    ..  code:: json
    
        {
            "enrollmentMessageType": "enroll",
            "enrollmentRequest": {
                "clientMessageID": "466548",
                "deviceId": "25b794-29a-4acb-9485-5a643d231f8U",
                "issuerId": "100502",
                "primaryAccountNumber": "8557530112345699"
            }
        }
            
    **Response:**
    
    ..  code:: json
    
        {
            "deviceId": "25b794-29a-4acb-9485-5a643d231f8U",
            "msgDeliveryStatus": [
                {
                    "code": "CHES101",
                    "message": "Card Holder enrolled Successfully"
                }
            ]
        }        
    """
    ATTRS = [
        'enrollmentMessageType',
        'enrollmentRequest',
    ]

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr in self.ATTRS and value:
                self.__setattr__(attr, value)

    class EnrollmentRequest(object):
        """Enrollment Request data object model.
        
        Part of :func:`~pyvdp.mlc.enrollment.EnrollmentsModel`.
        
        :param str clientMessageID: **Required**. Unique message identifier. 29 characters string.
        :param str primaryAccountNumber: **Required**. Cardholder PAN to be enrolled or deenrolled. Max 19 characters
            string.
        :param str deviceId: **Required**. Device identifier for enrollment. Must be globally unique. Recommended to
            use `UUID Version 1 <https://tools.ietf.org/html/rfc4122>`_. Max 50 characters string.
        :param str issuerId: **Required**. Issuer ID provided by Visa during onboarding. 6 digits string.
        """
        ATTRS = [
            'clientMessageID',
            'deviceId',
            'issuerId',
            'primaryAccountNumber',
        ]

        def __init__(self, **kwargs):
            for attr, value in kwargs.items():
                if attr in self.ATTRS and value:
                    self.__setattr__(attr, value)
