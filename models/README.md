# OntoMind Models

This directory contains lightweight, domain-adaptive language models for ontological reasoning.

## Structure

- `ontomind-50m/`  
  - Pretrained OntoMind-50M model (50M parameters)  
  - `config.json`: model hyperparameters  
  - `pytorch_model.bin`: weights (GPL-3.0-only)  
  - `onto_vocab.txt`: base vocabulary (32,000 canonical terms)  

- `ontomind.py`: model class with `from_pretrained()`  
- `tokenizer/`:  
  - `dynamic_onto_tokenizer.py`: builds runtime vocab from onto144 + domain lexicon  
  - `build_vocab.py`: utility to regenerate base vocab from incubation corpus  

## License

All model weights and code are licensed under **GPL-3.0-only**.  
No training on user data. Training corpus derived solely from `data/incubation/` (canonical representative texts).