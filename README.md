# CSE 576 - Commonsense Dataset Generation

## Steps
1) Install dependencies via 
`pip install -r requirements.txt`  with python >=3.6.
Make sure you have the stopwords corpus downloaded with 
```python -c "import nltk; nltk.download('stopwords')"```

2) Construct the input file for the UNILM QG model using the `build_input.py` file.

3) Set up the python environment for UNILM and follow the instructions for using the unilm-v1/src/biunilm/decode_seq2seq.py file to pass the created file as a non-tokenized input (don't include the `--tokenized_input` flag).

4) Combine the generated question output using the provided `combine_data.py` file in this repository to a csv file.

**Note:** There is some debugging required to get the microsoft/unilm repo to work on most machines and some intstructions are msising that should be included such as pip installing botocore after running `pip install --user --editable .` in the src folder.

## Citations
- Wikipedia article design inspired by a presentation given by Catherine Henry at 2017 Clearwater DevCon
  - https://www.youtube.com/watch?v=3vRZ6dBPL2A&t=1177s

- Unified Language Model Pre-training for Natural Language Understanding and Generation
  - See the [paper](https://papers.nips.cc/paper/9464-unified-language-model-pre-training-for-natural-language-understanding-and-generation.pdf)
  - Or visit the [Microsoft Github implementation](https://github.com/microsoft/unilm)