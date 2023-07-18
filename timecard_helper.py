import json
import re
import datetime
from datetime import datetime

class Email:
    client_list = ['TRSC', 'VABC', 'CROC', 'EXLD']
    counter_case = 0
    counter_code = 0
    
    def __init__(self, file_name):
        self.file_name = file_name
        
    def open_file(self):
        f = open(self.file_name)
        data = json.load(f)
        f.close()
        
        return data
        
    def get_subject(self): # Review to see if this qualifies for staticmethod
        subject_list = []
        
        for i in self.open_file()['value']:
            subject_list.append(i['subject'])
        
        return subject_list
    
    def get_date(self):
        date_list = []
        for i in self.open_file()['value']:
            date = datetime.strptime(i['sentDateTime'],"%Y-%m-%dT%H:%M:%SZ").date()
            date_list.append(date)

        return date_list
        
    def get_case_number(self):
        case_number_list = []
        
        for i in self.get_subject():
            case_number = re.findall(r'(\d{6})', i) # at this point case_number is a list type
            no_subject = "UNKNOWN Case Number"
            if case_number:
                for x in case_number:
                    case_number_str = ""
                    case_number_str += x
                    case_number_list.append(case_number_str)
            else: # Have to have this logic for client code
                Email.counter_case+=1
                counter_str = str(Email.counter_case)
                no_subject += counter_str
                case_number_str = no_subject
                case_number_list.append(case_number_str)

        return case_number_list
    
    def get_client_code(self):
        client_code_list = []
        
        for i in self.get_subject():
            client_code = re.findall(r'(\S{4})', i)
            
            for x in client_code: # At this point nested list is called
                client_code = x.upper()
                if client_code in Email.client_list: # If match is found the for loop breaks here
                    break
                    
                elif client_code not in Email.client_list: # Here match is not found - clean up the addition
                    #print(type(Email.counter_code))
                    no_client_code = "UNKNOWN Client Code"
                    Email.counter_code+=1
                    counter_str = str(Email.counter_code)
                    no_client_code += counter_str
                    no_client_code_result = no_client_code
                    client_code = None
    
            if client_code is not None:
                client_code_list.append(client_code)
            else:
                client_code_list.append(no_client_code_result)
        return client_code_list
    
    def get_client_code_and_case_number(self):
        case_number_list = self.get_case_number()
        client_code_list = self.get_client_code()
        if len(case_number_list) == len(client_code_list):
            result = dict(zip(case_number_list, client_code_list))
        else:
            result = "UNKNOWN ERROR"
        return result

    def get_final_list(self): # this will return a nested dictionary: {Date: [case#:client code, case#:client code]...}
        date_list = self.get_date()
        client_code_case_number_dict = self.get_client_code_and_case_number()

        resulting_dict = {}

        for (date, cc_case_num) in zip(date_list, client_code_case_number_dict.items()):
            dict_entry = dict(date = cc_case_num)
            print(dict_entry)

            if date in resulting_dict:
                resulting_dict[date].append(cc_case_num)

            elif date not in resulting_dict:
                resulting_dict.update(dict_entry)

        return resulting_dict


            # my_dict = {'key': [1, 2, 3]}
            # my_dict['key'].append(4)  # This method can be used if date already exists in the dictionary
            # print(my_dict)  # Output: {'key': [1, 2, 3, 4]}