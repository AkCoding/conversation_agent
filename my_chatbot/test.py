import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Function to check if a given text is a person's name
def is_person_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return True
    return False

# Test examples
examples = ["my name is bharat, The error occurs because the en_core_web_sm model is not installed in your environment. spaCy requires you to download the model explicitly before using it.", "it's Apple Inc.", "my name is Mount Everest", "i am Alice"]
for example in examples:
    print(f"{'example'}: {'Person Name' if is_person_name(example) else 'Not a Person Name'}")
