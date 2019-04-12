This script aims to support humans in filling due diligence survey. For each question from the survey, it looks for the best corresponding question in a DB. It leverages basic NLP paradigms like "lemming" and "tokenization". 

The script uses console user input to trigger functionalities like changing the question manually or looking for the right answer using keywords. The script relies on CSV file which need to be deployed in the same folder as the script.

Please note that the script has been developed for Windows and has not been tested on other platforms.

## Modules
* main.py - the core module
* cosine.py - where comparison is processed using NLP paradigms
* fileprocessing.py - manage IO

## Files
Those are mandatory files and must be encoded in UTF8 (in case you are on windows)
* config.json - where key variables are stored - the idea is to make the script improvable, e.g. by adding new stopwords
* db.csv - ['question','answer'] - the DB with all existing questions and answers
* questions.csv - ['question'] - the survey containing all questions
* output.csv - [id, question, ratio, db.question, db.answer] - the output generated, the ratio is the success ratio (is set to 1 in case the element has been manually set)

## Key functions
* main.initial_run() - a fully automated search - based on the questions (questions.csv) it will look for the best suitable corrsponding question in the DB and create the output (output.csv)
* main.manual_run(question) - is used to look for a question which has been manually input
* main.work_on_result() - based on percentiles the user can improve the search for a dedicated set of questions, e.g. all questions which don't match a minimal success ratio of 0.2. Then the user can improve the search for a given question using different options: (a) look for 5 different alternatives, (b) enter a question manually, e.g. to change the wording and (c) look for an answer using cumulative keywords. Once the user finds an acceptable answer the output is modified and the success ratio is set to the maximum.

## Key data structures
* cfg_data - created from the configuration file - contains all configuration variables
* list_q - list of questions extracted from questions.csv
* list_db - the DB extracted from db.csv

## Workflow
Note that the output is systematically updated and can be used out of the shell once produced - in case the script should be killed the output is never lost. The script can be started again without lost.

(1) Start the script using python3 ".\main.py"  
(2) Choose if you want to run the script for all questions or improve the questions manually (or both)  
(3) If you choose to improve the result  
    (3.1) Enter the threshold (minimal success ratio) - all questions under the threashold will be selected  
    (3.2) Identify the question you want to work on using an ID  
    (3.3) Choose the option a, b or c (see above)  
        (3.3.a) 5 Alternatives are identified, you can select the best match using an ID  
        (3.3.b) Enter a question manually - 5 alternatives are identified - you can select the best match using an ID   
        (3.3.c) You can use keywords to look for answers - keywords are cumulative which means questions must contain all keywords - you can restart the process at any time - you can enter more than one keyword at a time using a ','  
        
## Changes

* file names for "questions", "db" and "output" can be set in the configuration file