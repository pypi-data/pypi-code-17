import copy

import classify_extractions

class DigExtractionsClassifier():

    def __init__(self, model, classification_field, embedding):
        self.renamed_input_fields = 'tokens'
        self.classification_field = classification_field
        self.model = model
        self.embedding = embedding
        self.metadata = {"classifier": "DigExtractionsClassifier"}
        self.extractor = classify_extractions.ClassifyExtractions(self.model, self.classification_field, self.embedding)

    def classify(self, extractions):
        if(self.classification_field in extractions):
            self.extractor.classify(extractions[self.classification_field])
        
        return extractions

    def get_metadata(self):
        """Returns a copy of the metadata that characterizes this extractor"""
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        """Overwrite the metadata that characterizes this extractor"""
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        """Return a scalar or ordered list of fields to rename to"""
        return self.renamed_input_fields
