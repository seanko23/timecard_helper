import timecard_helper # this grabs the timecard_helper file

object = timecard_helper.Email('sample_json_message.json')

#print(object.get_client_code_and_case_number()) # calls get_client_code_and_case_number function and prints the result
# print(object.get_final_list())
# print(object.get_user_defined_date())



# print(object.get_final_list_cleanup())

# print(object.get_json_output())
print(object.cleaned_output_in_a_file())
# print(object.get_number_of_unknowns())
# print(object.get_case_number())
# print(object.get_subject())