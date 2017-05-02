import codecs
import json
import os
import sys
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digTokenizerExtractor.tokenizer_extractor import TokenizerExtractor

def load_embeddings(filename):
    filename = get_file_from_resources(filename)
    print filename
    embeddings = dict()
    print "Loading Embeddings..."
    with codecs.open(filename, 'r', 'utf-8') as f:
        for line in f:
            obj = json.loads(line)
            for k, v in obj.items():
                embeddings[k] = v
    return embeddings

def get_full_filename(current_file, filename):
    return os.path.join(os.path.dirname(current_file), filename)

def get_file_from_resources(filename):
    cwd = os.getcwd()
    return os.path.join(cwd, 'resources', filename)

def tokenize(text, method = 'dig'):
    tokens = list()

    if(method == 'nltk'):
        for s in sent_tokenize(text):
            word_tokens += word_tokenize(s)

    elif(method == 'dig'):
        doc = { 'string': text}
        e = TokenizerExtractor()
        ep = ExtractorProcessor().set_input_fields('string').set_output_field('output').set_extractor(e)
        updated_doc = ep.extract(doc)
        word_tokens = updated_doc['output'][0]['result'][0]['value']

    return word_tokens

def value_to_lower(token):
    token['value'] = token.get('value').lower()

def get_extractions_of_type(token, classification_field):
    extracted_semantic_types = list()
    semantic_types = token.get('semantic_type')
    if(semantic_types is not None):
        for semantic_type in semantic_types:
            type = semantic_type.get('type')
            if(type == classification_field):
                #Is of the same type. Check whether it has offset = 0
                offset = semantic_type.get('offset')
                if(offset is not None and offset == 0):
                    extracted_semantic_types.append(semantic_type)

    return extracted_semantic_types

def get_length_of_extraction(semantic_type):
    length = semantic_type.get('length')
    if(not length):
        length = 1
    return length

def get_context(tokens, index, length, context_range, use_word_in_context):
    token = tokens[index]
    extraction_starting = index
    extraction_ending = index + length - 1
    context_lower_index = max(0,index - context_range)
    context_upper_index = min(len(tokens) - 1, extraction_ending + context_range)
    context = list()
    for i in range(context_lower_index, context_upper_index + 1):
        if(i >= extraction_starting and i <= extraction_ending):
            #Word is itself the extraction
            if(use_word_in_context):
                context.append(tokens[i])
        else:
            context.append(tokens[i])

    return context

def get_vector_of_context(context, embeddings):
    context_vector = None
    for token in context:
        word = token['value']
        if word not in embeddings: # is the word even in our embeddings?
            continue

        current_vector = embeddings[word]  # Get the embeddings of the word
        if not context_vector:
            context_vector = current_vector
        else:
            context_vector = map(lambda x, y : x+y, context_vector, current_vector)
    
    if(context_vector):
        return np.array(context_vector)
    else:
        print "Have no context in the embeddings"
        #Need to implement prior probability or increase the size of the window dynamically
        return np.array(embeddings.values()[0]) #Getting vector of any word in the dictionary
