# Import libraries:
import csv
import os
import urllib.request, json 
from urllib.request import urlopen, Request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# gspread stuff (https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
# After that, search Google Sheets API and enable it as well.

print('\nGetting credentials from json...')

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('control-panel.json', scope)
client = gspread.authorize(creds)

print('\nOpening spreadsheet...')

cp = client.open("Lisbon October 2019 Data Analytics Full Time | Control Panel v1.0")

labs = cp.get_worksheet(9)

lab_cp = dict(zip([labs.cell(2,i).value for i in range(4,63)], list(range(4,63))))

users = {'mjvsilva':3, 'juliette-l':4, 'Mariana427':5, 'lukessmalley':6, 'Felipe-Hub':7, 'luisbsaude':8,
         'frankcardozo':9, 'EvelienDonkers':10, 'Juanlacalle':11, 'Constanze05':12, 'dandoye':13,
         'MattiaLobascio':14}

# Get links:

print('\nAdding links to txt...')

with open('lab_names.txt', 'r') as f:
    reader = csv.reader(f)
    lab_names = [name.strip("\'") for name in list(reader)[0]]

path1 = 'https://api.github.com/repos/ta-data-lis/'
path2 = '/pulls?state=open'

with open('links.txt', 'w', newline='') as myfile:
#          wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#          wr.writerow(path1 + lab_name + path2)
    for lab_name in lab_names:
        myfile.write(",\"" + path1 + lab_name + path2 + "\"")
print('\nlinks.txt has been filled')

with open('links.txt', 'r') as f:
    reader = csv.reader(f)
    page_list = list(reader)[0][1:]
    

# Do the job:    

token = '5e71cf50d45536be4e0ea4d94a5c70419d69fc72'

zeroes = [] # labs with 0 open pull requests

print('\nGetting labs info...\n\n\n')

for url in page_list:
    
    lab_name = url[39:].strip('pulls?state=open').strip('/')
    request = Request(url)
    request.add_header('Authorization', 'token %s' % token)
    response = urlopen(request)
    # print(response.read())
    data = json.loads(response.read().decode())

    count = 0
    
    lab_links = []
    
    for i in range(13):
    
        try:
            user = data[i]['user']['login']
            lab_links.append('[' + data[i]['user']['login'] + ']' + '  ' + data[i]['html_url'])
            
            # Writes Delivered in Control Panel
            labs.update_cell(users[user], lab_cp[lab_name], 'Delivered')            
            
        except:
            break
            
    count = i
    if not count:
        zeroes.append(lab_name)
        
    else:
        print('\n' + str(count) + ' open PR for ' + lab_name + ':\n')
        lab_links.reverse()
        print(*lab_links,sep='\n')

# print('\n\n' + str(len(zeroes)) + ' labs with 0 PR.')
      
print('\n\nHave a good time checking!\n')
