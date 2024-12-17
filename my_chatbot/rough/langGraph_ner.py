import os
import json
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import shutil
import json
from typing import List, Dict

class EntityRecognizer:
    def __init__(self, model_path: str):
        """
        Initialize the EntityRecognizer with a spaCy model.
        :param model_path: Path to the directory containing the trained spaCy NER model.
        """
        try:
            self.nlp = spacy.load(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            raise ValueError(f"Failed to load model from {model_path}: {e}")

    def recognize_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Recognize named entities in the given text using the loaded NER model.

        :param text: The input text for entity recognition.
        :return: A list of dictionaries containing the entities, their labels, and spans.
        """
        if not hasattr(self, 'nlp'):
            raise ValueError("Model is not loaded. Ensure the correct model path is provided.")

        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start_char': ent.start_char,
                'end_char': ent.end_char
            })
        return entities

    # # Recognize entities in a sample text
    # text = "Apple is looking at buying U.K. startup for $1 billion."
    # entities = recognizer.recognize_entities(text)


class NERTrainer:
    def __init__(self, base_config_path='/home/wappnet-12/PycharmProjects/Conversational_ai_bot/base_config.cfg', config_path='/home/wappnet-12/PycharmProjects/Conversational_ai_bot/config.cfg'):
        """
        Initialize NER Trainer with configuration paths
        """
        self.base_config_path = base_config_path
        self.config_path = config_path

    def prepare_training_data(self, annotations, output_path='training_data.spacy'):
        """
        Prepare training data from annotations
        """
        nlp = spacy.blank("en")
        db = DocBin()

        for text, annot in tqdm(annotations):
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in annot["entities"]:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    print(f"Skipping entity in text: {text}")
                else:
                    ents.append(span)
            doc.ents = ents
            db.add(doc)

        db.to_disk(output_path)
        print(f"Training data saved to {output_path}")

    def create_node_model(self, node_name, annotation_file):
        """
        Create a dedicated NER model for a specific node
        """
        # Create node directory
        node_dir = os.path.join('models', node_name)
        os.makedirs(node_dir, exist_ok=True)

        # Load annotations
        with open(annotation_file, 'r') as f:
            annotations_data = json.load(f)

        # Prepare training data
        train_data_path = os.path.join(node_dir, 'training_data.spacy')
        self.prepare_training_data(
            annotations_data.get('annotations', []),
            output_path=train_data_path
        )

        # Copy configuration files
        shutil.copy(self.base_config_path, os.path.join(node_dir, 'base_config.cfg'))
        shutil.copy(self.config_path, os.path.join(node_dir, 'config.cfg'))

        # Train command
        train_command = (
            f"python -m spacy train {os.path.join(node_dir, 'config.cfg')} "
            f"--output {node_dir} "
            f"--paths.train {train_data_path} "
            f"--paths.dev {train_data_path}"
        )

        print(f"\nTraining model for node: {node_name}")
        print("Run the following command in terminal:")
        print(train_command)

        # Optional: Automatically run training
        try:
            import subprocess
            print("\nStarting model training...")
            result = subprocess.run(train_command, shell=True, check=True)
            print(f"Model for {node_name} trained successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Training failed for {node_name}: {e}")

#
# def load_workflow_config(config_path):
#     """
#     Load workflow configuration
#     """
#     with open(config_path, 'r') as f:
#         return json.load(f)


def find_annotation_files(node):
    """
    Find annotation file for a specific node
    """
    # node_name = node['name']
    # Naming convention: {node_name}_annotations.json
    possible_files = [
        f"{node}_annotations.json",
        f"{node}.json"
    ]

    # Write the data to a .json file
    with open(possible_files[0], "w") as json_file:
        json.dump(json_file, indent=4)

    print(f"Data successfully written to {possible_files[0]}")


    for file in possible_files:
        if os.path.exists(file):
            return file

    return None


def train_workflow_ner_models(annotation_file_path):
    """
    Train NER models for all nodes in workflow
    """
    # Create models directory
    os.makedirs('models', exist_ok=True)

    # Load workflow configuration
    # workflow_config = load_workflow_config(workflow_config_path)

    # Initialize NER Trainer
    ner_trainer = NERTrainer()

    # Iterate through workflow nodes
    # for node in workflow_config['workflow']['nodes']:

    # if len(node['trainingPhrases']) == 0:
    #     continue
    node_name = "NAME"

    node_name = node_name.replace(" ", "_")

    # Find annotation file
    # annotation_file = find_annotation_files(node_name)
    annotation_file = annotation_file_path

    if annotation_file:
        print(f"Found annotations for node {node_name}: {annotation_file}")
        ner_trainer.create_node_model(node_name, annotation_file)
    else:
        print(f"No annotations found for node: {node_name}")


if __name__ == "__main__":
    # Usage
    train_workflow_ner_models("PERSON_annotations.json")