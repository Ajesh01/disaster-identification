# Import and load the spacy model
import spacy
nlp=spacy.load("en_core_web_sm") 

# Getting the ner component
ner=nlp.get_pipe('ner')

# New label to add
LABEL = "FOOD"

# Training examples in the required format
TRAIN_DATA =[ ("Pizza is a common fast food.", {"entities": [(0, 5, "FOOD")]}),
              ("Pasta is an italian recipe", {"entities": [(0, 5, "FOOD")]}),
              ("China's noodles are very famous", {"entities": [(8,14, "FOOD")]}),
              ("Shrimps are famous in China too", {"entities": [(0,7, "FOOD")]}),
              ("Lasagna is another classic of Italy", {"entities": [(0,7, "FOOD")]}),
              ("Sushi is extemely famous and expensive Japanese dish", {"entities": [(0,5, "FOOD")]}),
              ("Unagi is a famous seafood of Japan", {"entities": [(0,5, "FOOD")]}),
              ("Tempura , Soba are other famous dishes of Japan", {"entities": [(0,7, "FOOD")]}),
              ("Udon is a healthy type of noodles", {"entities": [(0,4, "ORG")]}),
              ("Chocolate soufflé is extremely famous french cuisine", {"entities": [(0,17, "FOOD")]}),
              ("Flamiche is french pastry", {"entities": [(0,8, "FOOD")]}),
              ("Burgers are the most commonly consumed fastfood", {"entities": [(0,7, "FOOD")]}),
              ("Burgers are the most commonly consumed fastfood", {"entities": [(0,7, "FOOD")]}),
              ("Frenchfries are considered too oily", {"entities": [(0,11, "FOOD")]})
           ]
ner.add_label(LABEL)

# Resume training
optimizer = nlp.resume_training()
move_names = list(ner.move_names)

# List of pipes you want to train
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

# List of pipes which should remain unaffected in training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]


from spacy.util import minibatch, compounding
import random

# Begin training by disabling other pipeline components
with nlp.disable_pipes(*other_pipes) :

  sizes = compounding(1.0, 4.0, 1.001)
  # Training for 30 iterations     
  for itn in range(30):
    # shuffle examples before training
    random.shuffle(TRAIN_DATA)
    # batch up the examples using spaCy's minibatch
    batches = minibatch(TRAIN_DATA, size=sizes)
    # ictionary to store losses
    losses = {}
    for batch in batches:
      texts, annotations = zip(*batch)
      # Calling update() over the iteration
      nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
      print("Losses", losses)


from pathlib import Path
output_dir=Path('/content/')

# Saving the model to the output directory
if not output_dir.exists():
  output_dir.mkdir()
nlp.meta['name'] = 'my_ner'  # rename model
nlp.to_disk(output_dir)
print("Saved model to", output_dir)

# Loading the model from the directory
print("Loading from", output_dir)
nlp2 = spacy.load(output_dir)
assert nlp2.get_pipe("ner").move_names == move_names
doc2 = nlp2(' Dosa is an extremely famous south Indian dish')
for ent in doc2.ents:
  print(ent.label_, ent.text)