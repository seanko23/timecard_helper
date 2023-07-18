import timecard_helper # this grabs the timecard_helper file

object = timecard_helper.Email('sample_json_message.json')

#print(object.get_client_code_and_case_number()) # calls get_client_code_and_case_number function and prints the result
print(object.get_final_list())
print(object.get_date())
#print(object.get_client_code())