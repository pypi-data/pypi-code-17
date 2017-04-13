from restclients_core import models


class GradebookParticipant(models.Model):
    participant_id = models.IntegerField()
    person_id = models.CharField(max_length=100)
    class_grade = models.CharField(max_length=250)
    notes = models.CharField(max_length=5000)

    def json_data(self):
        return {"participant_id": self.participant_id,
                "person_id": self.person_id,
                "class_grade": self.class_grade,
                "notes": self.notes}
