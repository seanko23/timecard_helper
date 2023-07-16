import json
import re

class Email:
    client_list = ['TRSC', 'VABC', 'CROC', 'EXLD']
    
    def __init__(self, file_name):
        self.file_name = file_name
        
    def open_file(self):
        f = open(self.file_name)
        data = json.load(f)
        f.close()
        
        return data
        
    def get_subject(self): # not calling open_file here, may need to adjust. Looking into it 
        #also reviewing if this qualifies for staticmethod
        subject_list = []
        
        for i in self.open_file()['value']:
            subject_list.append(i['subject'])
        
        return subject_list
    
    def get_date(self):
        pass
        

    def get_case_number(self):
        case_number_list = []
        
        for i in self.get_subject():
            case_number = re.findall(r'(\d{6})', i) # at this point case_number is a list type

            for x in case_number:
                case_number_str = ""
                case_number_str += x
                case_number_list.append(case_number_str)
            
        return case_number_list
    
    def get_client_code(self):
        client_code_list = []
        
        for i in self.get_subject():
            case_number = re.findall(r'(\d{6})', i)
            client_code = re.findall(r'(\S{4})', i)

            for x in client_code: # At this point nested list is called
                client_code = x.upper()
                if client_code in Email.client_list: # If match is found the for loop breaks here
                    break
                    
                elif client_code not in Email.client_list: # Here match is not found
                    no_client_code = "UNKNOWN"
                    client_code = None
    
            if client_code is not None:
                client_code_list.append(client_code)
            else:
                client_code_list.append(no_client_code)
        return client_code_list
    
    def get_client_code_and_case_number(self):
        result = dict(zip(self.get_case_number(), self.get_client_code()))
        return result

# The end result should look like this: {Date: [case#:client code, case#:client code]...}
# Maybe I want to grab the subject as well

print(Email('sample_json_message.json').get_client_code_and_case_number())
#print(Email('sample_json_message.json').get_subject())