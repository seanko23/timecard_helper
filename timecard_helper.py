import json
import re
from datetime import (
    datetime,
    timedelta
)
import app_constants

class Email:
    client_list = app_constants.client_list
    date_list = app_constants.date_list
    counter_case = 0
    counter_code = 0
    client_list_error = "Please check if each client code is 4 letters each"
    date_list_error = "Please check if date format is correct"
    
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
            date_str = date.strftime("%y-%m-%d")
            date_list.append(date_str)

        return date_list
    
    def client_list_validator(self):
        for i in Email.client_list:
            if len(i) != 4:
                return False
            else:
                pass
        return True
    
    def get_user_defined_date(self):
        delta = timedelta(days=1)
        format = '%y-%m-%d'
        date_list = Email.date_list
        new_date_list = []

        if not date_list: # if date_list is empty return an empty list
            pass
        else:
            for i in date_list:
                try:
                    datetime.strptime(i, format)
                except ValueError:
                    return Email.date_list_error
        for i in range(len(date_list)):
            if i == 0:
                new_date_list.append(date_list[i])
                x = 0
            while new_date_list[-1] != date_list[-1]:
                date_entry = datetime.strptime(new_date_list[x], format)
                new_datetime = date_entry.date()+delta
                date_str = new_datetime.strftime("%y-%m-%d")
                new_date_list.append(date_str)
                x+=1
            else:
                pass
        
        return new_date_list
        
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
        checker = self.client_list_validator()

        if checker == False:
            return False
        elif checker == True:
            for i in self.get_subject():
                res1 = " ".join(re.findall("[a-zA-Z]+", i))
                client_code = re.findall(r'(\S{4})', res1)
                
                for x in client_code: # At this point nested list is called
                    client_code = x.upper()
                    if client_code in Email.client_list: # If match is found the for loop breaks here
                        break
                        
                    elif client_code not in Email.client_list: # Here match is not found - clean up the addition
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
        checker = self.client_list_validator()
        if checker == False:
            return False
        elif len(case_number_list) == len(client_code_list):
            result = dict(zip(case_number_list, client_code_list))
        else:
            result = "UNKNOWN ERROR"
        return result

    def get_final_list(self): # this will return a nested dictionary: {Date: [case#:client code, case#:client code]...}
        date_validator = self.get_user_defined_date()
        checker = self.get_client_code_and_case_number()
        checker_unknown = "UNKNOWN ERROR"
        if checker == checker_unknown:
            return checker
        elif checker == False:
            return Email.client_list_error
        else:
            date_list = self.get_date()
            case_number_list = self.get_case_number()
            client_code_list = self.get_client_code()

            resulting_dict = {}

            for (date, case_number, client_code) in zip(date_list, case_number_list, client_code_list):
                dict_entry = dict(casenumber = client_code)
                dict_entry[case_number] = dict_entry['casenumber']
                del dict_entry['casenumber']
                dict_entry = [dict_entry] # making the dictionary entry into list to be appendable

                final_dict_entry = dict(date = dict_entry)
                final_dict_entry[date] = final_dict_entry['date']
                del final_dict_entry['date']

                if date in resulting_dict:
                    resulting_dict[date].append(dict_entry) # There is [] around each entry where final_dict_entry doesn't

                elif date not in resulting_dict:
                    resulting_dict.update(final_dict_entry)

            new_resulting_dict = {key: [item for sublist in value for item in (sublist if isinstance(sublist, list) else [sublist])]
                    for key, value in resulting_dict.items()} #Explanation below

            sorted_resulting_dict = sorted(new_resulting_dict.items(), key=lambda x:x[0], reverse=False) # Order the output in date asc manner
            converted_dict = dict(sorted_resulting_dict)

            # return converted_dict
            removable_dates = []
            if not date_validator:
                return converted_dict
            elif date_validator == Email.date_list_error:
                return Email.date_list_error
            else:
                for date, information in converted_dict.items():
                    if date not in date_validator:
                        removable_dates.append(date)
                    else:
                        pass
                for i in removable_dates:
                    del converted_dict[i]
                return converted_dict
        
            #{key: value for key, value in resulting_dict.items()} -> Iteratehrough each key-value pair in the original dictionary
            
            #new_resulting_dict = {key: [item for item in value] for key, value in resulting_dict.items()} 
            # -> For each key-value pair, we iterate through the value, which is a list of dictionaries.

    def get_final_list_cleanup(self): # Removes UNKNOWN values from get_final_list()
        if self.get_final_list() == Email.client_list_error:
            return Email.client_list_error
        elif self.get_final_list() == Email.date_list_error:
                return Email.date_list_error
        else:
            identifier = "UNKNOWN"
            input = self.get_final_list()
            output = {
                date: [{key: value} for item in value_list for key, value in item.items() if identifier not in key and identifier not in value]
                for date, value_list in input.items()
            }
            return output

    
    def get_json_output(self): # Returns JSON format with UNKNOWN values
        if self.get_final_list() == Email.client_list_error:
            return Email.client_list_error
        elif self.get_final_list() == Email.date_list_error:
                return Email.date_list_error
        else:
            output = self.get_final_list()
            return json.dumps(output, indent = 4)
    
    def get_cleanup_output(self): # Returns JSON format without UNKNOWN values
        if self.get_final_list_cleanup() == Email.client_list_error:
            return Email.client_list_error
        elif self.get_final_list() == Email.date_list_error:
                return Email.date_list_error
        else:
            output = self.get_final_list_cleanup()
            return json.dumps(output, indent = 4)


    def get_number_of_unknowns(self): #get count of emails where both client code and case number are unknowns
        input = self.get_final_list() # gets the finalized list
        identifier = "UNKNOWN"
        
        if input == Email.client_list_error:
            return Email.client_list_error
        elif input == Email.date_list_error:
                return Email.date_list_error
        else:
            for date, information in input.items():
                totally_unknown = 0
                case_counter = 0
                client_counter = 0
                case_str = ""
                client_str = ""
                for val in information:
                    for key, value in val.items():
                        if identifier in key and identifier in value:
                            totally_unknown += 1
                            continue
                        elif identifier in key:
                            if case_counter > 0:
                                client_str+=", "
                            case_counter += 1
                            client_str+=value
                            continue
                        elif identifier in value:
                            if client_counter > 0:
                                case_str+=", "
                            client_counter += 1
                            case_str+=key
                            continue

                if totally_unknown > 0 or case_counter > 0 or client_counter > 0:
                    print(f"On {date}: ")
                    if totally_unknown > 0:
                        print(f"{totally_unknown} email(s) without any notable information")
                    elif case_counter > 0:
                        print(f"{case_counter} email(s) without case number(s) for {client_str}")
                    elif client_counter > 0:
                        print(f"{client_counter} email(s) where case numbers are: {case_str} without client code")
                    print("\n")
                else:
                    pass
