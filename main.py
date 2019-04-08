#cd OneDrive\qna\program
import cosine
import fileprocessing
import re
import sys
import colorama
from colorama import Fore, Style
colorama.init()

cfg_data = fileprocessing.read_json() #get config data
home = cfg_data['default']['home']
list_q = []
list_db = []

cosine_ob = '' #initiate the object

#h_p_x functions should help printing information in the console
#this is a simple helper function to print textual information - improve standardization
def h_p_console(level, txt=''):
    #level 1 - information
    if level == 1:
        print('')
        print("{:-^40s}".format(txt), end='\n\n')
     #level 2 - error
    elif level == 2:
        print("ERROR >> " + txt, end='\n\n')
    elif level == 3:
        print("INFO >> " + txt, end='\n\n')
        

#print colored keywords [] out of s string
def h_p_color(string, keywords): 
    
    #note: because the word is replaced with the input from user, we might lost upper case if the word is at beginning of the sentence
    for k in keywords:
        insensitive_k = re.compile(re.escape(k), re.IGNORECASE)
        string = insensitive_k.sub(Fore.YELLOW+k+Style.RESET_ALL, string)
        
    return string
    
# --- end h_p_x functions ---
    
    
#using keywords to identify the best suitable answer - if inexistant return ''
#origin defined from where the function has been called (standalone or extended)
def sys_exit():
    print('')
    h_p_console(1,"Goodbye !!!")
    fileprocessing.write_json(cfg_data)
    sys.exit()
    
def search_keyWords(origin='extended'):
    
    input_list = [x[1] for x in list_db]
    
    list_keywords = []
    
    keyword = 'start'
    while keyword != '':
        if origin != 'standalone':
            h_p_console(1, "2.2.0 Cumulative Keywords Search")
            h_p_console(3, "Nbre of answers found in DB: " + str(len(input_list)))
            keyword = input("Please enter \n[Keyword(s)] you want to search - use ',' as separator \n[b]          Back to main menu \n[s]          New search \n[Inx]        If for a prefered option:\n>> ")
            
            if keyword == 'b':
                h_p_console(1)
                return ''
        else:
            h_p_console(1, "Cumulative Keywords Search")
            h_p_console(3, "Nbre of answers found in DB: " + str(len(input_list)))
            keyword = input("Please enter \n[Keyword(s)] you want to search - use ',' as separator \n[s]          New search \n>> ")
        

        if keyword == 's':
            list_keywords = []
            input_list = [x[1] for x in list_db]
        elif len(keyword) < 3 or not keyword:
            try:
                if not keyword:
                    h_p_console(1)
                    return ''
                else:
                    h_p_console(1)
                    return input_list[int(keyword)]
            except:
                h_p_console(2,"Please make sure to enter a digit which is smaller than 3 char or a keyword bigger than 3 char")
                pass
        else:
            k = keyword.split(',')
            list_keywords += k
            for i in k:
                input_list = [x for x in input_list if i.lower() in x.lower()] #look for the keyword in the response
            
            input_list = list(set(input_list))
            
            h_p_console(1)
            print("Number of instances found: " + str(len(input_list)))
            
            if len(input_list) > 0:
                
                if len(input_list) > int(cfg_data['default']['nb_responses_displayed']): #if less than 5 - is automatically displayed
                    output = input("How many instances do you want to print out: ")
                    if not output:
                        output = '1'
                    print('')
                else:
                    output = '5'
                
                try:
                    output = int(output)
                except:
                    h_p_console(2, "No digit - apply 1 per default")
                    output = '1'
                    
                h_p_console(1)
                for ix, i in enumerate(input_list[:int(output)]):
                    print(Fore.CYAN+"{:4s} {:<2d}".format('Inx', ix)+Style.RESET_ALL)
                    print("{:<s}".format( h_p_color(i, list_keywords)))
                
            else:
                input_list = [x[1] for x in list_db]


def initial_run():
    
    global cosine_ob
    
    cosine_ob = cosine.Cosine(list_db) 
    output_list = [] #[[q_id, q, ratio, db.q, db.a]] - focus only on the best ratio
    
    try:
        list_q = fileprocessing.read_csv('questions.csv')
    except:
        h_p_console(2, "The file with questions does not exist - please refer to documentation")
        sys_exit()
    
    #for q in list_q[:2]: #[:2] used to limit the number of iteration while testing
    for q_id, q in enumerate(list_q):
        question = q[0]
        #best_fit = compare.run_check(question,list_db) #[[r,q,a],[r,q,a]]
        best_fit = cosine_ob.main(question) #[[r,q,a],[r,q,a]]
        output_list.append([q_id]+[question]+best_fit[0]) #only the best ratio - this part should be adapted if we want all result
        q_id += 1 #to define the id of the question
            
    fileprocessing.write_csv('output.csv',output_list)

#used to pass a question
def manual_run(question):
    
    global cosine_ob
    
    if cosine_ob == '': #object not initialized
        cosine_ob = cosine.Cosine(list_db) 
    
    best_fit = cosine_ob.main(question, 5)
    #best_fit = compare.run_check(question,list_db, 5) #[[r,q,a],[r,q,a]]
    
    h_p_console(1, "5 Alternatives")
    
    for ix, i in enumerate(best_fit): #index is used to make choice possible
        print(Fore.CYAN+"{:4s} {:<2d} - {:4s} {:.2f}".format('Inx', ix, 'Ratio', i[0])+Style.RESET_ALL)
        print('Q_db: ' + i[1])
        print('R_db: ' + i[2])
        
    return best_fit
    
def work_on_result():
    
    load_output = fileprocessing.read_csv('output.csv') #[[q_id, q, ratio, db.q, db.a]]

    #compute ratio distribution
    list_r = []
    [list_r.append(float(x[2])) for x in load_output]
    
    import numpy as np
    h_p_console(1, "Percentiles")
    print("Percentiles: 10, 25, 50, 75, 90 >> ", end='')
    print([round(x,2) for x in np.percentile(list_r, [10, 25, 50, 75, 90])])

    ratio_min = input("All questions with a ratio < [x.yy] will be manually reviewed: ")
    h_p_console(1)
    if not ratio_min:
        ratio_min = 1

    #work on questions with a ratio smaller than the one which is defined
    while True:
    
        nb_questions = 0
        for inx, x in enumerate(load_output): #Note: we nmust loop on all elements because we are modifying the list
            if float(x[2]) <= float(ratio_min):
                nb_questions += 1
                print("{:4s} {:<4d} - {:4s} {:.2f}".format('Q_id', inx, 'Ratio', float(x[2])))
                print('Q_in: ' + x[1])
                print('Q_db: ' + x[3], end='\n\n')
        
        if nb_questions == 0:
            break

        inx_digit = False
        question_context = ''
        while not inx_digit:
            h_p_console(1)
            inx = input("Enter the [Q_id] for a manual search: ")
            question_context = str(inx)
            try:
                inx = int(inx)
                break
            except:
                print("Please enter a digit")

        while True:
            h_p_console(1, '2.0.0 Manual Search')
            print("QUESTION: " + load_output[inx][1], end='\n\n')
            choice = input('[0] - Look for 5 different alternatives \n[1] - Enter a modified question manually \n[2] - Key words search in response:\n[3] - Back to list of questions\n>> ')

            if choice == '0':
            #look for 5 different alternatives
                #inx = 0
                h_p_console(1,"2.1.0 Existing Alternatives")
                new_search = manual_run(load_output[inx][1]) #[[r,q,a],[r,q,a]]

                input_res = input("Choose the best option [inx] or [n] for a new search: ")
                #input_res = 1
                if input_res == 'n' or not input_res:
                    pass
                else:
                    input_res = int(input_res)
                    oa = load_output[inx] #[q_id, q, ratio, db.q, db.a] - extract from load_output
                    oa[2] = '1'
                    oa[3] = new_search[input_res][1]
                    oa[4] = new_search[input_res][2]

                    fileprocessing.write_csv('output.csv',load_output) #save a copy
                    break #exit the while

            elif choice == '1':
            #add the question manually and complete same process - replace the q_db question with this one in the file
                h_p_console(1,"2.2.0 Manual Question")
                question_manual = input("Please enter the question manually, 5 alternatives will be looked up: ")
                new_search = manual_run(question_manual) #[[r,q,a],[r,q,a]]

                input_res = input("Choose the best option [inx] or [n] for a new search: ")
                #input_res = 1
                if input_res == 'n' or not input_res:
                    pass
                else:
                    input_res = int(input_res)
                    oa = load_output[inx] #[q_id, q, ratio, db.q, db.a] - extract from load_output
                    oa[2] = '1'
                    oa[3] = new_search[input_res][1]
                    oa[4] = new_search[input_res][2]

                    fileprocessing.write_csv('output.csv',load_output) #save a copy
                    break #exit the while

            elif choice == '2':
            #look for an answer using key words
                response = search_keyWords() #db.q, db.a
                if response == '':
                    pass
                else:
                    oa = load_output[inx] #[q_id, q, ratio, db.q, db.a] - extract from load_output
                    oa[2] = '1'
                    oa[3] = oa[1] #in this case we don't consider the db.q as we are looking directly for the response, furthermore the db as more than one question for a same answer
                    oa[4] = response

                    fileprocessing.write_csv('output.csv',load_output) #save a copy
                    break
            else:
                break

try:
    list_db = fileprocessing.read_csv('db.csv')
except:
    h_p_console(2, "The file with DB does not exist - please refer to documentation")
    sys_exit()

#Can be commented depending on what we want to do

try:
    h_p_console(1,"Welcome")
    to_do = input("Do you want to:\n[1] - Run the script to find the best options \n[2] - Refine the result  \n[3] - Both sequentially \n[4] - Search responses with keywords\n>> ")
    if to_do == '1':
        print("... Please be patient - it might take a while", end='\n\n')
        initial_run()
        print("... Completed the script is closing")
    elif to_do == '2':
        work_on_result()
    elif to_do == '4':
        search_keyWords('standalone')
    else:
        print("... Please be patient - it might take a while", end='\n\n')
        initial_run()
        work_on_result()

except KeyboardInterrupt:
    sys_exit()

sys_exit()