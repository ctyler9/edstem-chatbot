import json
import os
from tqdm import tqdm
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from vars import REGDATA_ROOT, ANONDATA_ROOT

INPATH_ROOT, OUTPATH_ROOT = REGDATA_ROOT, ANONDATA_ROOT

### Anon Function 
# Set up the engines, loads the NLP module (spaCy model by default) 
# and other PII recognizers
# done globally so not repeat process each function call
g_analyzer = AnalyzerEngine()
g_anonymizer = AnonymizerEngine()

# supported entities: https://microsoft.github.io/presidio/supported_entities/

def anonymize_text(text: str, entities: list=["PHONE_NUMBER", "PERSON", "EMAIL_ADDRESS", "CREDIT_CARD", "DATE_TIME", "IP_ADDRESS", "NRP", "LOCATION", "URL"]) -> str:
    # Call analyzer to get results
    results = g_analyzer.analyze(text=text,
                               entities=entities,
                               language='en')

    # Analyzer results are passed to the AnonymizerEngine for anonymization
    anonymized_text = g_anonymizer.anonymize(text=text,analyzer_results=results)

    return anonymized_text.text

### Anon Data
def anonymize_json_data(in_path: str, out_path: str) -> None:
    with open(in_path, 'r') as infile, open(out_path, 'w') as outfile:
        json_block = json.load(infile)

        anon_threadposts = "" 
        anon_comments = ""
        new_json_list = []
        for entry in tqdm(json_block):
            if "threadPost" in entry:
                try:
                    anon_threadposts = anonymize_text(entry["threadPost"])
                except:
                    pass
            if "comments" in entry:
                # excuse gross code, really annoying edge cases 
                try: 
                    comments = entry["comments"]
                    if isinstance(comments, list) and any(isinstance(sublist, list) for sublist in comments):
                        for x in comments:
                            if type(x) == list:
                                x = [anonymize_text(y) for y in x]
                            else:
                                x = x
                            anon_comments.append(anonymize_text(x))
                        anon_comments = [[anonymize_text(y) for y in x] for x in comments]
                    else:
                        anon_comments = [anonymize_text(x) for x in comments]
                except: 
                    pass

            new_json_block = {"threadPost": anon_threadposts, "comments": anon_comments}
            new_json_list.append(new_json_block)

        # Write the list of dictionaries to the output file
        json.dump(new_json_list, outfile, indent=2)  # Use indent for pretty formatting


if __name__ == "__main__":
    ## DATA ANONYMIZATION
    text = "My name is Tom Meyers and my phone number is 212-555-5555 and my email is tmeyers@gmail.com. You can find my work at https://www.youtube.com/watch?v=MfGTdQ7nPzQ."
    #print(anonymize_text(text))

    ## CLEAN DATA
    
    infiles = os.listdir(INPATH_ROOT)
    for file in infiles:
        inpath = os.path.join(INPATH_ROOT, file)
        outpath = os.path.join(OUTPATH_ROOT, file)

        anonymize_json_data(inpath, outpath)

