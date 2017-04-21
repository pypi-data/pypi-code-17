from pyvdp.mlc.dispatcher import VisaMobileLocationConfirmationDispatcher


def send(data):
    """Submits MLC Enrollment request.
    
    :param pyvdp.mlc.enrollment.EnrollmentsModel data: Instance of MLC Enrollment model.
    :return: Response from VDP
    
    **Usage:**
    
    ..  code:: python
        
        from pyvdp.mlc.enrollment import enrollments, EnrollmentsModel
        
        request_kwargs = {
            "clientMessageID": "466548",
            "deviceId": "25b794-29a-4acb-9485-5a643d231f8U",
            "issuerId": "100502",
            "primaryAccountNumber": "8557530112345699"        
        }
        
        data_kwargs = {
            "enrollmentMessageType": "enroll",
            "enrollmentRequest": EnrollmentsModel.EnrollmentRequest(**request_kwargs)        
        }
        
        data = EnrollmentsModel(**data_kwargs)
        result = enrollments.send(data)
        print(result)
    """
    c = VisaMobileLocationConfirmationDispatcher(resource='mlc',
                                                 api='enrollment',
                                                 method='enrollments',
                                                 http_verb='POST',
                                                 data=data)
    return c.send()
