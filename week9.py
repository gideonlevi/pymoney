import sys

def initialize():
    try:
        fh = open("records.txt", 'r')
        print("Welcome back!")
        balance = int(fh.readline()[:-1]) #read balance
        record_input = fh.readlines() #read records
        fh.close()
        #i[:-1] to remove the newline char, split and save as tuple in a list
        records_list = [tuple(i[:-1].split(' ')) for i in record_input]
        try: #check value
            for i in records_list:
                test_int = int(i[2])
        except:
            raise ValueError
    except ValueError: #Invalid format in records
        balance = 0 #set to 0 by default
        #print error in stderr
        sys.stderr.write("Invalid format in records.xtx. Deleting the contents.\n")
        try:
            #initialize List to store all records
            records_list = []  
            #input balance
            balance = int(input('How much money do you have? '))
        except:
            balance = 0
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
    except FileNotFoundError: #Can't open file
        try:
            #initialize List to store all records
            records_list = []  
            #input balance
            balance = int(input('How much money do you have? '))
        except:
            balance = 0
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
    return balance, records_list
        
def add(records_list, categories):
    #input expense or income
    input_str = input('Add an expense or income record with description and amount:\n')
    #separate each expense or income
    records_str = input_str.split(', ')
    #separate description and amount
    try:
        for v in records_str:
            catg, desc, amn = v.split(' ')
            try: #check for invalid value
                assert is_category_valid(catg, categories)
                test_int = int(amn)
            except ValueError: #amn invalid value
                sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
                continue
            except AssertionError:
                sys.stderr.write("Category is not valid.\nFail to add a record.\n")
                continue
                
            #if records_list not empty
            if bool(records_list): #any
                records_list.append(tuple([catg, desc, amn]))
            #if empty
            else:
                records_list = [tuple([catg, desc, amn])]
    #wrong input format exception
    except ValueError:
        sys.stderr.write("The format of a record should be like this: meal breakfast -50.\nFail to add a record.\n")
    return records_list

def view(balance, records_list):
    catg_width = 18
    desc_width = 14
    amn_width = 10
    amount = 0 #total amount of expenses and income
    #output
    print("Here's your expense and income records:")
    print(f"  {'Category':{catg_width}} {'Description':{desc_width}}{'  Amount':>{amn_width}}")
    print(f"{'-'*(catg_width+desc_width+amn_width+4)}")
    #if records_list is not empty
    if bool(records_list): #any
        #records list
        for index, i in enumerate(records_list):
            print(f"{index+1}  {i[0]:<{catg_width}}{i[1]:<{desc_width}}{i[2]:>{amn_width}}")
        #accumulate amount of expense and income
        amount = sum(int(i[2]) for i in records_list)
    print(f"{'-'*(catg_width+desc_width+amn_width+4)}")
    print(f"Now you have {balance + amount} dollars.")

def delete(records_list):
    #input mode
    del_mode = input("Select mode (single, multi, all): ")
    #single deletion mode
    if del_mode == 'single':
        try:
            del_arg = input('Input index: ')
            del records_list[int(del_arg)-1]
        except ValueError:
            sys.stderr.write("Invalid format of args.\nFormat should be like this: 2\n")
        except IndexError:
            sys.stderr.write("The specified record does not exist\n")
    #multi deletion mode
    elif del_mode == 'multi':
        try:
            del_arg = input('Input indices: ')
            del_list = del_arg.split(' ')
            del_list.sort() #sort from lowest to highest
            for i in del_list[::-1]:
                del records_list[int(i)-1]  
        except ValueError:
            sys.stderr.write("Invalid format of args.\nFormat should be like this: 1 4 7\n")
        except IndexError:
            sys.stderr.write("The specified record does not exist\n")
    #all deletion mode
    elif del_mode == 'all':
        try:
            del_arg = input("Input record category, description, and amount: ")
            del_catg, del_desc, del_amn = del_arg.split(' ')
            try: #check for invalid value
                test_int = int(del_amn)
            except ValueError:
                sys.stderr.write("Invalid value for amount.\n")
                #return to escape
                return records_list
            #tag to tell wheter the specified record exist
            exist = False
            #delete all income with the same desc and amount from behind
            for idx, val in list(enumerate(records_list))[::-1]:
                if val[0] == del_catg and val[1] == del_desc and val[2] == del_amn:
                    exist = True
                    del records_list[idx]
            assert exist #check if the specified record exist
        except ValueError:
            sys.stderr.write("Invalid format of args.\nFormat should be like this: meal breakfast -50\n")
        except AssertionError: #specified record in all mode does not exist
            sys.stderr.write("The specified record does not exist\nFail to delete record.\n")
    else: #invalid mode
        sys.stderr.write("Invalid mode (single, multi, all).\nFail to delete record.\n")
    return records_list
    

def exit(balance, records_list):
    #write in records.txt file
    with open('records.txt', 'w') as fh:
        #write balance in 1st line
        fh.write(f'{balance}\n')
        #if not empty
        if records_list:
            #write all records
            fh.writelines('\n'.join(i[0]+' '+i[1]+' '+i[2] for i in records_list) + '\n')

def initialize_categories():
    return ['expense', ['food', ['meal', 'snack', 'drink'], 
            'transportation', ['bus', 'railway']], 
            'income', ['salary', 'bonus']]

def view_categories(L, level=-1):
    if type(L) == list:
        for i in L:
            view_categories(i, level+1)
    else:
        print(f'{" "*4*level}-{L}')

def is_category_valid(category, categories):
    if type(categories) == list:
        for i in categories:
            if is_category_valid(category, i) == True:
                return True
    return category == categories

def find(categories):
    category = input('Which category do you want to find? ')
    print(find_subcategories(category, categories))
    view(balance, list(filter(lambda x: x[0] in find_subcategories(category, categories), records_list)))

def find_subcategories(category, categories):
    if type(categories) == list:
        for v in categories:
            p = find_subcategories(category, v)
            if p == True:
                index = categories.index(v)
                if index+1 < len(categories) and type(categories[index+1]) == list:
                    return flatten(categories[index:index + 2])
                else:
                    return [v]
            if p != []:
                return p
    return True if category == categories else []

def flatten(L):
    if type(L) == list:
        result = []
        for child in L:
            result.extend(flatten(child))
        return result
    return [L]

#initialize
balance, records_list = initialize()
categories = initialize_categories()

#main loop
while True:
    prompt = input("What do you want to do (add / view / delete / view categories / find / exit)?")
    if prompt == 'add':
        records_list = add(records_list, categories)
    elif prompt == 'view':
        view(balance, records_list)
    elif prompt == 'delete':
        records_list = delete(records_list)
    elif prompt == 'exit':
        exit(balance, records_list)
        break
    elif prompt == 'view categories':
        view_categories(categories)
    elif prompt == 'find':
        find(categories)
    else:
        sys.stderr.write('Unknown command.\n')
