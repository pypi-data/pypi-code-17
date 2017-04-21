from ml_buff.models.input_data import InputData

class BaseInputDataRepository():
    def get(self, session, input_data_id):
        return_value = (
            session.query(InputData)
            .filter(InputData.id == input_data_id)
            .one_or_none()
        )
        if return_value is not None:
            session.expunge(return_value)
        return return_value
