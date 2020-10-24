import wikipedia
from io import StringIO
from rake_nltk import Rake
from markdown import Markdown

import warnings
warnings.catch_warnings()
warnings.simplefilter("ignore")


RANDOM_PAGES_COUNT = 500                # number of total pages to explore
WIKIPEDIA_MAX_RANDOM_COUNT = 10         # the wikipedia module can only fetch limited random pages at once
MIN_CONTEXT_LENGTH = 30                 # in characters
KEY_WORD_SCORE_BOUNDARY = 3.0           # rake-nltk score


## No longer in use
## To patch markdown output on some Wikipedia pages
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False

def unmark(text):
    return __md.convert(text)



## Extract context-answer pairs here
## to be used as input for UNILM QG model

def main(output_file='input.pa.txt'):
    # Grab the summaries of RANDOM_PAGES_COUNT pages on Wikipedia
    paragraphs = []
    iterations = RANDOM_PAGES_COUNT // WIKIPEDIA_MAX_RANDOM_COUNT
    for i in range(iterations):
        pages = wikipedia.random(pages=WIKIPEDIA_MAX_RANDOM_COUNT)
        for page in pages:
            try:
                p_arr = wikipedia.summary(page).split("\n")
                paragraphs.extend([p for p in p_arr if len(p) > 30])
            except:
                pass


    # Uses stopwords for english from NLTK, 
    # and all puntuation characters by default
    r = Rake()

    ctxt_ans_combos = []
    for para in paragraphs:
        r.extract_keywords_from_text(para)
        keywords = [v for u,v in r.get_ranked_phrases_with_scores() if u > KEY_WORD_SCORE_BOUNDARY]
        if len(keywords) > 0:
            ctxt_ans_combos.extend([(para, x) for x in keywords])

    formatted_unilm_data = ["{0} [SEP] {1}".format(para, ans) for para, ans in ctxt_ans_combos]

    with open(output_file, 'wt', encoding='utf-8') as data_file:
        data_file.write('\n'.join(formatted_unilm_data))
    
    print('Successfully build {} with {} final lines.'.format(output_file, len(formatted_unilm_data)))

if __name__ == "__main__":
    main()