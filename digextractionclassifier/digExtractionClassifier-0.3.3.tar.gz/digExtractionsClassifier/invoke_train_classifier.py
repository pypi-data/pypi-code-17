import digExtractionsClassifier.train_classifier

EMBEDDING_FILE = 'unigram-part-00000-v2.json'
SEMANTIC_TYPE = 'city'
TRAINING_FILE = ''
DATA_FIELD = ''
trained_classifier = train_classifier.TrainClassifier(EMBEDDING_FILE, SEMANTIC_TYPE, classifier_type = 'random_forest', 
    input_data_type = 'tokens', tokenization_strategy = 'dig', semantic_types_marked = False, scale = False, normalize = True, k_best = False, 
    train_percent = 0.3, context_range = 5, use_word_in_context = True, use_break_tokens = False)

trained_classifier.train_classifier(TRAINING_FILE, DATA_FIELD, annotated_field = 'annotated_city', correct_field = 'correct_city', testing_file = None)
