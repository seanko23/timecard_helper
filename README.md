# timecard_helper

The goal of the Time Card Helper project is to decrease the amount of time people spend when entering timecards. From my person experience, the object is to reduce the timecard entry effort from 30 minutes to 10 or less minutes.
This is achieved by reading the sent file folder for user specified date. From the output JSON file, the goal is to just read the subject and sentDateTime attributes.

With some data processing, the program is able to output the statistical output of the email you have sent over the specified time period and the output should be able to assist the user with the time entry. Also, the output will provide Case number and Client Code which an user has worked on based on email subjects. Please see below for details on the sample output.

Sample json file exsts in this. The data format may change depending on the records returned with the Microsoft Graph API.

More information on Microsoft Graph to come


Sample output:
On 23-07-13: 
2 email(s) where case numbers are: 227514, 734862 without client code


On 23-07-15: 
1 email(s) without case number(s) for EXLD


On 23-07-11: 
2 email(s) without any notable information