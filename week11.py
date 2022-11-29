import sys

class Record:
    """Represent a record."""
    def __init__(self, catg, desc, amn):
        self._category = catg
        self._description = desc
        self._amount = amn
    @property
    def category(self):
        return self._category
    @property
    def description(self):
        return self._description
    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        # 1. Read from 'records.txt' or prompt for initial amount of money.
        # 2. Initialize the attributes (self._records and self._initial_money)
        #	from the file or user input.
        try:
            fh = open("records.txt", 'r')
            print("Welcome back!")
            balance = int(fh.readline()[:-1]) #read balance
            record_input = fh.readlines() #read records
            fh.close() #close file
            records_list = []
            #i[:-1] to remove the newline char, split and save as Record instance
            for v in record_input:
                catg, desc, amn = v[:-1].split(' ')
                try: #check value
                    test_int = int(amn)
                    r = Record(catg, desc, amn) 
                    records_list.append(r)
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
        self._records_list = records_list
        self._balance = balance

    def add(self, input_str, categories):
        # 1. Define the formal parameter so that a string input by the user
        #	representing a record can be passed in.
        # 2. Convert the string into a Record instance.
        # 3. Check if the category is valid. For this step, the predefined
        #	categories have to be passed in through the parameter.
        # 4. Add the Record into self._records if the category is valid.
        #separate each expense or income
        records_str = input_str.split(', ')
        #separate description and amount
        try:
            for v in records_str:
                catg, desc, amn = v.split(' ')
                try: #check for invalid value
                    assert categories.is_category_valid(catg)
                    test_int = int(amn)
                    r = Record(catg, desc, amn) 
                except ValueError: #amn invalid value
                    sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
                    continue
                except AssertionError:
                    sys.stderr.write("Category is not valid.\nFail to add a record.\n")
                    continue
                    
                #if records_list not empty
                if bool(self._records_list): #any
                    self._records_list.append(r)
                #if empty
                else:
                    self._records_list = [r]
        #wrong input format exception
        except ValueError:
            sys.stderr.write("The format of a record should be like this: meal breakfast -50.\nFail to add a record.\n")

    def view(self):
        # 1. Print all the records and report the balance.
        catg_width = 18
        desc_width = 14
        amn_width = 10
        amount = 0 #total amount of expenses and income
        #output
        print("Here's your expense and income records:")
        print(f"  {'Category':{catg_width}} {'Description':{desc_width}}{'  Amount':>{amn_width}}")
        print(f"{'-'*(catg_width+desc_width+amn_width+4)}")
        #if records_list is not empty
        if bool(self._records_list):
            #records list
            for index, r in enumerate(self._records_list):
                print(f"{index+1}  {r.category:<{catg_width}}{r.description:<{desc_width}}{r.amount:>{amn_width}}")
            #accumulate amount of expense and income
            amount = sum(int(r.amount) for r in self._records_list)
        print(f"{'-'*(catg_width+desc_width+amn_width+4)}")
        print(f"Now you have {self._balance + amount} dollars.")

    def delete(self, del_arg):
        # 1. Define the formal parameter.
        # 2. Delete the specified record from self._records.
        try:
            del self._records_list[int(del_arg)-1]
        except ValueError:
            sys.stderr.write("Invalid format of args.\nFormat should be like this: 2\n")
        except IndexError:
            sys.stderr.write("The specified record does not exist\n")

    def find(self, categories):
        # 1. Define the formal parameter to accept a non-nested list
        #	(returned from find_subcategories)
        # 2. Print the records whose category is in the list passed in
        #	and report the total amount of money of the listed records.
        # 1. Print all the records and report the balance.
        catg_width = 18
        desc_width = 14
        amn_width = 10
        amount = 0 #total amount of expenses and income
        #output
        print("Here's your expense and income records:")
        print(f"  {'Category':{catg_width}} {'Description':{desc_width}}{'  Amount':>{amn_width}}")
        print(f"{'-'*(catg_width+desc_width+amn_width+4)}")
        #if records_list is not empty
        if bool(self._records_list):
            #records list
            for index, r in enumerate(self._records_list):
                if r.category in categories:
                    print(f"{index+1}  {r.category:<{catg_width}}{r.description:<{desc_width}}{r.amount:>{amn_width}}")
            #accumulate amount of expense and income
            amount = sum(int(r.amount) for r in self._records_list if r.category in categories)
        print(f"{'-'*(catg_width+desc_width+amn_width+4)}")
        print(f"Total amount in the listed records: {amount} dollars.")

    def save(self):
        with open('records.txt', 'w') as fh:
            #write balance in 1st line
            fh.write(f'{self._balance}\n')
            #if not empty
            if self._records_list:
                #write all records
                fh.writelines('\n'.join(r.category+' '+r.description+' '+r.amount for r in self._records_list) + '\n')    

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 
            'transportation', ['bus', 'railway']], 
            'income', ['salary', 'bonus']]
 
    def view(self):
        def rec_view_categories(L, level):
            if type(L) == list:
                for i in L:
                    rec_view_categories(i, level+1)
            else:
                print(f'{" "*4*level}-{L}')
        rec_view_categories(self._categories, -1)    

    def is_category_valid(self, category):
        def rec_is_category_valid(category, categories):
            if type(categories) == list:
                for i in categories:
                    if rec_is_category_valid(category, i) == True:
                        return True
            return category == categories
        return rec_is_category_valid(category, self._categories)
 
    def find_subcategories(self, category):
        def rec_find_subcategories(category, categories):
            if type(categories) == list:
                for v in categories:
                    p = rec_find_subcategories(category, v)
                    if p == True:
                        index = categories.index(v)
                        if index+1 < len(categories) and type(categories[index+1]) == list:
                            return self._flatten(categories[index:index + 2])
                        else:
                            return [v]
                    if p != []:
                        return p
            return True if category == categories else []
        return rec_find_subcategories(category, self._categories)    
 
    def _flatten(self, L):
        def rec_flatten(L):
            if type(L) == list:
                result = []
                for child in L:
                    result.extend(rec_flatten(child))
                return result
            return [L]
        return rec_flatten(L)


#initialize
records = Records()
categories = Categories()

#main loop
while True:
    prompt = input("What do you want to do (add / view / delete / view categories / find / exit)?")
    if prompt == 'add':
        record = input('Add an expense or income record with description and amount:\n')
        records.add(record, categories)
    elif prompt == 'view':
        records.view()
    elif prompt == 'delete':
        del_arg = input('Which record do you want to delete? ')
        records.delete(del_arg)
    elif prompt == 'view categories':
        categories.view()
    elif prompt == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif prompt == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Unknown command. Try again.\n')
