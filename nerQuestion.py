import nltk
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

#ONLY DOWNLOAD AT THE BEGINING IF THEY DOES NOT EXIST IN THE SYSTEM
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

def extract_entity_question (question):

    sample = question
    sentences = nltk.sent_tokenize(sample) #split in to sentences
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences] #split in to words
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences] #tag sentences with NN, NNP, etc
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:
        # Print result tree
        # print tree
        # Print results per sentence
        # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))

    # Print all entity names
    # print entity_names

    # Remove incorrect entity "which"
    if 'Which' in entity_names:
        entity_names.remove('Which')
    if 'which' in entity_names:
        entity_names.remove('Which')

    # Print unique entity names
    # print set(entity_names)
    return entity_names

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE': # NE means Named Entity
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def replace_entity_name(question, entity):
    # Replace entity into "entity"
    newQuestion = question.replace(entity[0], "\"entity\"")
    return newQuestion