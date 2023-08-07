# timecard_helper

How to use Postman and Microsoft Graph API: https://learn.microsoft.com/en-us/graph/use-postman#step-2-download-the-postman-agent-optional---postman-web-browser-only

The goal of the Time Card Helper project is to decrease the amount of time people spend when entering timecards. From my person experience, the object is to reduce the timecard entry effort from 30 minutes to 10 or less minutes.
This is achieved by reading the sent file folder for user specified date. From the output JSON file, the goal is to just read the subject and sentDateTime attributes.

With some data processing, the program is able to output the statistical output of the email you have sent over the specified time period and the output should be able to assist the user with the time entry. Also, the output will provide Case number and Client Code which an user has worked on based on email subjects. Please see below for details on the sample output.

Sample json file exsts in this. The data format may change depending on the records returned with the Microsoft Graph API.

Each individual user may need to set up Azure access for this feature.

Usage of app_constrants.py file:
1. User should define the expected list of client codes
2. User should define the beginning and end dates for which the result to populate on if not done so during Postman API



Sample output:
On 23-07-13: 
2 email(s) where case numbers are: 227514, 734862 without client code


On 23-07-15: 
1 email(s) without case number(s) for EXLD


On 23-07-11: 
2 email(s) without any notable information

Another Ex.
{
    "23-07-11": [
        {
            "123456": "VABC"
        },
        {
            "772262": "VABC"
        }
    ]
}