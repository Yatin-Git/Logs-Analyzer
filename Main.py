from os import close
import re
import sys
import pandas as pd
#creating empty lists initially
date = []
time = []
serial_number = []
ip_address = []
user_agent = []
status_code = []
req_type = []
api = []
user = []
enterprise_id = []
enterprise_name = []
s = 1
#opening file
file_name = sys.argv[1]
file = open(file_name, 'r')
a = []
# function to extract the logs by matching the pattern in string 
def extract_everything(str):
    result1 = re.match(r'\s?(.*)\s\d+:\d+:\d+', str)
    date.append(result1.group(1))

    result2 = re.search(r'\s(\d+:\d+:\d+),\d+',str)
    time.append(result2.group(1))

    result3 = re.search(r'IP-Address=(.*)#,!User-Agent', str)
    ip_address.append(result3.group(1))

    result4 = re.search(r"User-Agent=(.*)\s*\(", str)
    user_agent.append(result4.group(1))

    result5 = re.search(r"!Request-Type=(.*)#,!API", str)
    req_type.append(result5.group(1))

    result6 = re.search(r"!API=(.*)#,!User-Login", str)
    api.append(result6.group(1)) 

    result7 = re.search(r"!User-Name=(.*)#,!EnterpriseId", str)
    user.append(result7.group(1)) 

    result8 = re.search(r"!EnterpriseId=(.*)#,!Enterprise", str)
    enterprise_id.append(result8.group(1)) 

    result9 = re.search(r"!EnterpriseName=(.*)#,!Auth", str)
    enterprise_name.append(result9.group(1)) 

    result10 = re.search(r"!Status-Code=(.*)#,!Response", str)
    status_code.append(result10.group(1)) 
# converting paragraphs into one single line string starting from date till Body=
while True:
    line = file.readline()
    if line:
        if re.match(r'\s?\d+-\d+-\d+',line):
            while line:
                if re.search(r'-Body=',line):
                    a.append(line)
                    break
                a.append(line.replace("\n",""))
                line = file.readline()
            t = "".join(a)
            extract_everything(t)
            serial_number.append(s)
            s=s+1
    else:
        break      

file.close()
# creating data frame and appending the columns
df = pd.DataFrame()
df['S No.'] = serial_number
df['DATE'] = date
df['TIME'] = time
df['IP-ADDRESS'] = ip_address
df['USER AGENT'] = user_agent
df['STATUS CODE'] = status_code
df['REQUEST TYPE'] = req_type
df['API'] = api
df['USER'] = user
df['ENTERPRISE-ID'] = enterprise_id
df['ENTERPRISE-NAME'] = enterprise_name
df.to_excel('Final.xlsx', index=False) 