# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 19:11:04 2020

@author: lcavo
"""
#SECTION 1: creating a dictionary for selected columns

import csv
with open('C:\\Users\\lcavo\\Desktop\\Final_project_ok\\Collections_csv\\C1645_StanBritt_Collection.csv', newline='', encoding="ISO-8859-1") as csvfile:
    reader = csv.DictReader(csvfile)
    
    wanted_columns = ["87.1", "87.2", "260", "246", "490", "$<icat1:3>", "301"]
    
    main_dict={} #empty dictionary for the full collection
    for row in reader: #we iterate over all rows of the csv file
        
        sub_dict = {} #we create a sub dictionary which will contain all the column names and their values for each ID number (CKEYs)
        for col in wanted_columns: #this for loops iterates in the wanted column list
            sub_dict[col] = row[col] #and makes the key of our subdictionary the column names, and the values are what is under those columns

       
        if row["1"] != "": #if column '1' is not empty
            main_dict[row["1"]] = sub_dict #then consider the values of column 1 the key of the T9 dictionary, and consider the sub dictionary the values of the T9dict
#print(main_dict)

#SECTION 2: establish what the current date is and what the recording date to consider for calculations will be
            
from datetime import datetime #we import the datetime module
for recording_key, recording_value in main_dict.items(): #for loops iterating over each key and over each value of the T9 dictionary
    recording_date = recording_value["260"] #we store all instances under value '260' in a variable called 'recording date'  
    len_recording_date = len(recording_date) #we are storing here the number of digits a date is composed of 
    
    if len_recording_date == 10: #if the recording date is 10 digits
        historical_date = datetime.strptime(recording_date, '%d/%m/%Y').date() #the strptime converts a string into a date format. It takes two arguments: the string to parse, and its format
    #elif len_recording_date == 7: #This piece of code can be reactivated when we find a way to express month and year only as a datetime object 
        #historical_date = datetime.strptime(recording_date, '%Y-%m').date() #reactivate when solution is found
    else:
        historical_date = None
    
    main_dict[recording_key]["usable_date"] = historical_date #we add a key to our dictionary called 'usable date' whose values will be the ones in the historical_date variable (datetime_object values)
    
    current_date = datetime.today().date() #we indicate what the current date is
    main_dict[recording_key]["current_date"] = current_date #we add a key to our dicitonary called 'currente_date'. Its values will be the values of the variable called current_date
    
#print(main_dict)

#SECTION 3: set up conditions for an anniversary to occur 
    
    if historical_date is None: #here we want to make sure that if historical date is not valid or empty
        day_difference = None #then our anniversary related variables will be null (None is Python's equivalent for null)
        is_full_anniversary = None 
        next_anniversary_date = None 
        days_to_anniversary = None
        anniversary_year = None
    else:
        day_difference = (main_dict[recording_key]["current_date"] - 
                          main_dict[recording_key]["usable_date"]).days #the variable day_difference will be the difference between dateobject current date MINUS the historical date
                          
        is_same_day = False
        if historical_date.day == current_date.day: #if the day of the historical date is equal to the day of the current date our variable 'is_same_day' will be flagged
            is_same_day = True
        
        is_same_month = False
        if historical_date.month == current_date.month:
            is_same_month = True
        
        is_full_anniversary = False
        if is_same_day and is_same_month: #if same_day and same_month are True then we will have a full anniversary
            is_full_anniversary = True
            
        next_anniversary_date = datetime(
            current_date.year, historical_date.month, historical_date.day
            ).date() #here we want to define when the next anniversary will be. We need to select the current year, along with the historical month and the historical day
        if next_anniversary_date < current_date:
            next_anniversary_date = datetime(
            current_date.year + 1, historical_date.month, historical_date.day
            ).date() #if the anniversary has passed (hence is minor to the current date), then it needs to be reset to the following year. So this variable should take the current year and add 1 year to it)
            
        days_to_anniversary = (next_anniversary_date - current_date).days #this will tell us how many days are left to next anniversary so that it can be constantly monitored
        anniversary_year = next_anniversary_date.year - historical_date.year #this is to calculate how many years have elapsed. 50th anniversary, 40th anniversary etc. We subtract the current year to the historical one in order to calculate number of years elapsed
        
    main_dict[recording_key]["day_difference"] = day_difference #we add to our dictionary the key/column 'day_difference'
    main_dict[recording_key]["is_full_anniversary"] = is_full_anniversary #we add to the dictionary the boolean key 'is_full_anniversary'
    main_dict[recording_key]["next_anniversary_date"] = next_anniversary_date
    main_dict[recording_key]["days_to_anniversary"] = days_to_anniversary
    main_dict[recording_key]["anniversary_year"] = anniversary_year

#SECTION 4: establishing all the keys over which we will have to iterate in order to create a new spreadsheet in section 5. We want to have an ID column, plus all the columns which so far have been keys of the subdictionary (246, 260, 490 etc.)
import csv
   
keylist =[] #we create an empty list which will host the keys of the Main_dictionary (CKEY numbers). This will allow us to access and interrogate the list by index numbers (when we will need all the keys for our new excel file)
for key in main_dict.keys(): #we loop over the keys only, the keys of the T9 dictionary (all CKEY numbers)
    keylist.append(key) #then we add these keys to our list
    break #this will break the for loop after the first iteration, so as to have just the first key (the first CKEYnumber of the Main_dictionary)
first_key = keylist[0] #we access the first element of our list (CKEY numbers) by indicating index 0, and store into the variable 'first_key'.   
first_value = main_dict[first_key] #this is the subdictionary of the first item in our dictionary (Fiesta in a house in Cusco)
#print(first_value)

columns_names = ["id"] + list(first_value.keys()) #our columns names will be a new one called 'id', plus all the keys of the subdictionary (the subdictionary referring to the first CKEY number, but it could be any oter CKEY number) print(keylist)


#SECTION 5: exporting keys and values into a new csv file

with open('C:\\Users\\lcavo\\Desktop\\Final_project_ok\\Aims\\Aim1\\Output.csv', 'w+', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.DictWriter(myfile, fieldnames=columns_names) #this is how you write a csv file from a dictionary; different syntax; nodelimiter needed, you need to speicfy the fieldnames
    wr.writeheader() #part of the syntax found on the internet
 
    for row_id, row in main_dict.items(): #this means for key (CKEYnumbers), values (subdictionaries) in T9 (now t9 includes all anniversaries columns)
        row["id"] = row_id #the 'id' key/column of the subdictionary is going to be filled with the key of the T9 full dictionary (which will be the CKEYnumbers)
        wr.writerow(row) #this will fill al the excel columns with the values of the T9 dictionary
        

#SECTION 6: setting up e-mail notifications, what to include in the e-mail sent and the conditions to be met in order to send it

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email():
            fromaddr = "lXXXXXi@gmail.com" #sender
            toaddr = "lXXXXX@gmail.com" #recipient
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Alert: Recording Date Anniversary!"
            body = 'Recording Date Anniversary in one of the Sound Archive collections: ' + 'Item title: '+ title + '. ID number: ' + ckey +'. Anniversary: ' + anniversary_year + 'years. Duration:  ' + duration +' Collection name: ' + collection_name + '. Curatorial area: ' + curatorial_area + '.' 
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "XXXXXXX") #replace Xs with e-mail password
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()


import csv
with open('C:\\Users\\lcavo\\Desktop\\Final_project_ok\\Aims\\Aim1\\Output.csv', newline='', encoding="ISO-8859-1") as csvfile:
    reader = csv.DictReader(csvfile) 
    for row in reader:
        if row['is_full_anniversary']=='TRUE': #send e-mail if variable 'is_full_anniversary' (in csv 'Output')  is true
            title= row['246'] #if 'is_full_anniversary' is true then consider the title to put in the message body the values of column 246.
            ckey= row['id']
            duration=row['301']
            collection_name=row["490"]
            curatorial_area=row["$<icat1:3>"]
            anniversary_year = row['anniversary_year']
            print('sending email with Title: ' + title + '' + ckey)
            send_email()
    

