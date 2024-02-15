import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def analyze_text(text):
    """
    Function to analyze text using spaCy for basic NLP tasks such as
    tokenization and part-of-speech tagging.
    """
    doc = nlp(text)
    analysis_results = {
        'sentences': [],
        'tokens': [],
        'entities': []
    }

    for sentence in doc.sents:
        analysis_results['sentences'].append(sentence.text)
        for token in sentence:
            analysis_results['tokens'].append({
                'text': token.text,
                'pos': token.pos_,
                'lemma': token.lemma_
            })
        for ent in sentence.ents:
            analysis_results['entities'].append({
                'text': ent.text,
                'type': ent.label_
            })

    return analysis_results
