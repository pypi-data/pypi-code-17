import codecs
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, precision_recall_fscore_support

import digExtractionsClassifier.utility.functions as utility_functions
import digExtractionsClassifier.preprocessing.semantic_type_marker as semantic_type_marker
class TrainClassifier():

    def __init__(self, embedding_file, semantic_type, classifier_type = 'random_forest', input_data_type = 'tokens', tokenization_strategy = 'dig', semantic_types_marked = True, scale = False, normalize = True, k_best = False, train_percent = 0.3, context_range = 5, use_word_in_context = True, use_break_tokens = False):
        """
        :param embedding_file: The file name of the embeddings file. The file should be present in the resources folder 
        :param semantic_type: Example 'city', 'ethnicity'
        :param classsifier_type: Supports 'random_forest'
        :param input_data_type: 'text' or 'tokens'
        :param tokenization_strategy: 'dig' or 'nltk'. Only used when input_data_type = 'text'
        :param semantic_types_marked: Applicable only if input_data_type = 'tokens'. True, if the tokens list is marked with the semantic types. If False, need to provide annotated_field and correct_field while calling train_classifier
        :param scale: to scale the vectors or not
        :param normalize: to normalize the vectors or not
        :param k_best: to select k-best features from the vectors or not
        :param train_percent: the training data percentage. Used only if no testing file provided
        :return: None
        """
        self.embedding_file = embedding_file
        self.classifier_type = classifier_type
        self.input_data_type = input_data_type
        self.tokenization_strategy = tokenization_strategy
        self.scale = scale
        self.normalize = normalize
        self.k_best = k_best
        self.train_percent = train_percent
        self.context_range = context_range
        self.use_word_in_context = use_word_in_context
        self.use_break_tokens = use_break_tokens
        self.embeddings = utility_functions.load_embeddings(self.embedding_file)

    def train_classifier(self, training_file, data_field, annotated_field = None, correct_field = None, testing_file = None):
        """
        :param training_file: file for training the classifier. Should be a jlines file
        :param testing_file: file for testing the classifier. If provided will train on the whole training file and test on this file
        :return: None
        """
        self.validate_inputs(annotated_field, correct_field)
        testing_data = None
        training_data = self.extract_data_from_file(training_file, data_field, annotated_field, correct_field)
        if(testing_file):
            testing_data = self.extract_data_from_file(testing_file, data_field, annotated_field, correct_field)
        else:
            training_data, testing_data = self.separate_testing_data_from_training(training_data)

        training_vector_extraction = self.generate_vectors(training_data)
        testing_vector_extraction = self.generate_vectors(testing_data)

        classifier = _train_classifier(training_vector_extraction, self.classifier_type)
        _test_classifier(classifier, testing_vector_extraction)

    def validate_inputs(self, annotated_field, correct_field):
        if(self.input_data_type == 'tokens'):
            if(not semantic_types_marked):
                if(not annotated_field or not correct_field):
                    raise Exception "Need to pass annotated_field and correct_field if the semantic types are not marked"
        elif(self.input_data_type == 'text'):
            if(not annotated_field or not correct_field):
                    raise Exception "Need to pass annotated_field and correct_field as text is present as input field"
        else:
            raise Exception "Invalid value for input_data_type"
        #Need to add other validations


    def extract_data_from_file(self, file_name, text_data_field, annotated_field, correct_field):
        all_data = list()
        with codecs.open(file_name, 'r', 'utf-8') as f:
            for line in f:
                data = dict()
                json_obj = json.load(line)
                data['correct'] = json_obj[correct_field]
                if(input_data_type == 'text'):
                    data['tokens'] = utility_functions.tokenize(json_obj[text_data_field], self.tokenization_strategy)
                    data['annotated'] = json_obj[annotated_field]
                    semantic_type_marker.mark_semantic_types(data['tokens'], data['annotated'])
                else:
                    data['tokens'] = json_obj[text_data_field]
                    if(not self.semantic_types_marked):
                        data['annotated'] = json_obj[annotated_field]
                        semantic_type_marker.mark_semantic_types(data['tokens'], data['annotated'], self.semantic_type, self.tokenization_strategy)
                all_data.append(data)



        return all_data

    def separate_testing_data_from_training(self, training_data):
        return train_test_split(training_data, train_size=self.train_percent)

    def generate_vectors(self, all_data):
        vectors = list()
        labels = list()
        vector_extraction = {"vectors":vectors, "labels":labels}
        for data in all_data:
            tokens = data['tokens']
            correct_fields = data['correct']
            correct_fields = [x.lower() for x in correct_fields]
            for index, token in enumerate(tokens):
                utility_functions.value_to_lower(token)
                semantic_types = utility_functions.get_extractions_of_type(token, self.semantic_type)
                for semantic_type in semantic_types:
                    #There are extractions in the token of the same type
                    length = utility_functions.get_length_of_extraction(semantic_type)
                    context = utility_functions.get_context(tokens, index, length, self.context_range, self.use_word_in_context)
                    context_vector = utility_functions.get_vector_of_context(context, self.embeddings)
                    vectors.append(context_vector)
                    if(token.get('value') in correct_fields):
                        #This is the correct token annotation
                        labels.append(1)
                    else:
                        labels.append(0)
        vectors = np.matrix(vectors)
        return vector_extraction

    def _train_classifier(self, vector_extraction, classifier_model = 'random_forest'):
        """
        Take training data numpy matrices and compute a bunch of metrics. Hyperparameters must be changed manually,
        we do not take them in as input.

        :param vector_extraction:
        :param classifier_model:
        :return:
        """
        vectors = vector_extraction['vectors']
        labels = vector_extraction['labels']
        model = dict()

        if(self.scale):
            scaler = StandardScaler()
            scaler.fit(feature_vectors)
            feature_vectors = scaler.transform(feature_vectors)
            model['scaler'] = scaler

        if(self.normalize):
            normalizer = Normalizer()
            normalizer.fit(feature_vectors)
            feature_vectors = normalizer.transform(feature_vectors)
            model['normalizer'] = normalizer

        if(self.kBest):
            kBest = SelectKBest(f_classif, k=20)
            kBest = kBest.fit(feature_vectors, labels)
            feature_vectors = kBest.transform(feature_vectors)
            model['k_best'] = kBest

        if classifier_model == 'random_forest':
            classifier = RandomForestClassifier()
            classifier.fit(train_data, train_labels)
            model['classifier'] = classifier
        
        return model

    def _test_classifier(self, vector_extraction, classifier):
        feature_vectors = vector_extraction['vectors']
        actual_labels = vector_extraction['labels']

        if(feature_vectors.ndim == 1):
            # print "Reshaping the vector"
            feature_vectors = feature_vectors.reshape(1, -1)

        if('scaler' in self.model):
            print "Scaling"
            feature_vectors = self.model['scaler'].transform(feature_vectors)
        
        if('normalizer' in self.model):
            print "Normalizing"
            feature_vectors = self.model['normalizer'].transform(feature_vectors)

        if('k_best' in self.model):
            feature_vectors = self.model['k_best'].transform(feature_vectors)

        predicted_labels = model.predict(feature_vectors)

        _print_stats(actual_labels, predicted_labels)

    def _print_stats(self, actual_labels, predicted_labels):
        prf = ['Precision: ', 'Recall: ', 'F-score: ', 'Support: ']
        print 'Class 0\tClass 1'
        k = precision_recall_fscore_support(actual_labels, predicted_labels)
        for i in range(0, len(k)):
            print prf[i],
            print k[i]




        