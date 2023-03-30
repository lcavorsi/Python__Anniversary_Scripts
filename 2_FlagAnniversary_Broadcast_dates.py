# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:19:20 2020

@author: lcavo
"""

#SECTION 1: creating a dictionary with nested subdictionary for selected columns
import csv
with open('C:\\Users\\lcavo\\Desktop\\Final_project_ok\\Collections_csv\\XXXXXX.csv', newline='', encoding="ISO-8859-1") as csvfile: #replace Xs with csv file name
    reader = csv.DictReader(csvfile)
    
    wanted_columns = ["87.1", "87.2", "260", "246", "490", "470", "474", "$<icat1:3>", "301"]
    
    main_dict={} #empty dictionary for the full collection
    for row in reader: #we iterate over all rows of the csv file
        
        sub_dict = {} #we create a sub dictionary which will contain all the MARC tags and values
        for col in wanted_columns: #this for loops iterates in the wanted column list
            sub_dict[col] = row[col] #and makes the key of our subdictionary the column names, and the values are what is under those columns

       
        if row["1"] != "": #if column '1' is not empty
            main_dict[row["1"]] = sub_dict #then consider the column name the key of the Main dictionary dictionary, and consider its values the values of the sub dictionary dictionary
print(main_dict)

#SECTION 2: establish what the current date is and what the broadcast date to consider for calculations will be      
from datetime import datetime #we import the datetime module
broadcast_date_list=[] #we create a list here to store all the values under column '470'. 
split_dates_list=[] #we create an empty list to store
historical_date_broadcast=None     
for recording_key, recording_value in main_dict.items(): 
    broadcast_date=recording_value["470"] #the broadcast date will be the values under column '470'. THESE CONTAIN ALSO TV CHANNEL AND PROGRAM TIME INFORMATION. IT NEEDS SPLITTING. SEE BELOW
    if '?' in broadcast_date:
        broadcast_date='' #values for the broadcast_date_list will be empty if there is a question mark in the 470 field
        broadcast_date_list.append(broadcast_date)
    elif '-' in broadcast_date: #if there is an hyphen in the 470 field, then add the value to the broadcast_date_list
        broadcast_date_list.append(broadcast_date)
    else:
        broadcast_date='' #otherwise just set the cell to none
        broadcast_date_list.append(broadcast_date)
#print(broadcast_date_list)       
    for date in broadcast_date_list: #date is still a string
        
        split_broadcast_date=date.split(' ',4) #we are splitting the field '470' in elements separated by empty space        
        if len(split_broadcast_date)==0 or len(split_broadcast_date)==1 or len(split_broadcast_date)==2: #this is to overcome the 'index out of list' error
            split_dates_list.append('')
            continue
        usable_broadcast_date=split_broadcast_date[3] #the date will be the fourth element of the split string (the one where digits are usually hyphen separated)
        split_dates_list.append(usable_broadcast_date) 
    for date in split_dates_list:
        #print(date)
        if len(date)==10:
            historical_date_broadcast = datetime.strptime(date,'%Y-%m-%d').date() #we select only full dates, those with 10 digits
    #print(usable_broadcast_date)
    #print(split_dates_list)
    #print(historical_broadcast_date)
    
        current_date = datetime.today().date() #we indicate what the current date is
        main_dict[recording_key]["current_date"] = current_date #we add a key to our dicitonary called 'currente_date'. Its values will be the values of the variable called current_date

        main_dict[recording_key]["usable_date_broadcast"] = historical_date_broadcast #we add a key to our dictionary called 'usable date' whose values will be the datetime_object values
          
#print(main_dict)

#SECTION 3: set up conditions for an anniversary to occur
    anniversary_year_broadcast=None  
    if historical_date_broadcast is None: #here we want to make sure that if historical date is not valid or empty
        day_difference_broadcast = None #then our variable day_difference will be null (None is Python's equivalent for null)
        is_full_anniversary_broadcast = None 
        next_anniversary_date_broadcast = None 
        days_to_anniversary_broadcast = None
        anniversary_year_broadast = None
    else:
        day_difference_broadcast = (main_dict[recording_key]["current_date"] - 
                          main_dict[recording_key]["usable_date_broadcast"]).days #the variable day_difference will be the difference between dateobject current date - historical date
                          
        is_same_day_broadcast = False
        if historical_date_broadcast.day == current_date.day: #if the day of the historical date is equal to the day of the current date our variable is_same_day will be flagged
            is_same_day_broadcast = True
        
        is_same_month_broadcast = False
        if historical_date_broadcast.month == current_date.month:
            is_same_month_broadcast = True
        
        is_full_anniversary_broadcast = False
        if is_same_day_broadcast and is_same_month_broadcast: #if same_day and same_month are True then we will have a full anniversary
            is_full_anniversary_broadcast = True
            
        next_anniversary_date_broadcast = datetime(
            current_date.year, historical_date_broadcast.month, historical_date_broadcast.day
            ).date() #here we want to define when the next anniversary will be. We need to select the current year, along with the historical month and the historical day
        if next_anniversary_date_broadcast < current_date:
            next_anniversary_date_broadcast = datetime(
            current_date.year + 1, historical_date_broadcast.month, historical_date_broadcast.day
            ).date() #if the anniversary has passed (hence is minor to the current date, then it needs to be reset to next year. So this variable should take the current year and add 1 year)
            
        days_to_anniversary_broadcast = (next_anniversary_date_broadcast - current_date).days #this will tell us how many days are left to next anniversary so that it can be constantly monitored
        anniversary_year_broadcast = next_anniversary_date_broadcast.year - historical_date_broadcast.year #this is to calculate how many years have elapsed. 50th anniversary, 40th anniversary. We subtract the current year to the historical one
        
    main_dict[recording_key]["day_difference_broadcast"] = day_difference_broadcast #we add to our dictionary the key/column 'day_difference'
    main_dict[recording_key]["is_full_anniversary_broadcast"] = is_full_anniversary_broadcast #we add to the dictionary the boolean key 'is_full_anniversary'
    main_dict[recording_key]["next_anniversary_date_broadcast"] = next_anniversary_date_broadcast
    main_dict[recording_key]["days_to_anniversary_broadcast"] = days_to_anniversary_broadcast
    main_dict[recording_key]["anniversary_year_broadcast"] = anniversary_year_broadcast

#print(main_dict)

#SECTION 4: establishing all the keys over which we will have to iterate in order to create a new spreadsheet in section 5. We want to have an ID column, plus all the columns which so far have been keys of the subdictionary (246, 260, 490 etc.)
import csv

   
keylist =[] #we create an empty list which will host the keys of the Main dictionary dictionary (CKEY numbers). This will allow us to access and interrogate the list by index numbers (when we will need all the keys for our new excel file)
for key in main_dict.keys(): #we loop over the keys only, the keys of the Main dictionary dictionary (all CKEY numbers)
    keylist.append(key) #then we add these keys to our list
    break #this will break the for loop after the first iteration, so as to have just the first key (the first CKEYnumber of the Main_dictionary)
first_key = keylist[0] #we access the first element of our list (CKEY numbers) by indicating index 0, and store into the variable 'first_key'.   
first_value = main_dict[first_key] #this is the subdictionary of the first item in our dictionary (Fiesta in a house in Cusco)
#print(first_value)

columns_names = ["id"] + list(first_value.keys()) #our columns names will be a new one called 'id', plus all the keys of the subdictionary (the subdictionary referring to the first CKEY number, but it could be any oter CKEY number) 


#SECTION 5: exporting keys and values into a new csv file
with open('C:\\Users\\lcavo\\Desktop\\Final_project_ok\\Aims\\Aim1\\Output_Radio.csv', 'w+', encoding="ISO-8859-1", newline='') as myfile:
    wr = csv.DictWriter(myfile, fieldnames=columns_names) #this is how you write a csv file from a dictionary; different syntax; no delimiter needed, you need to speicfy the fieldnames
    wr.writeheader() #part of the syntax found on the internet
 
    for row_id, row in main_dict.items(): #this means for key (CKEYnumbers), values (subdictionaries) in Main dictionary (now Main dictionary includes all anniversaries columns)
        row["id"] = row_id #the 'id' key/column of the subdictionary is going to be filled with the key of the Main dictionary full dictionary (which will be the CKEYnumbers)
        wr.writerow(row) #this will fill al the excel columns with the values of the Main dictionary dictionary
        
#SECTION 6: setting up e-mail notifications, what to include in the e-mail sent and the conditions to be met in order to send it

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email():
            fromaddr = "XXXXX@gmail.com" #add here sender's e-mail address
            toaddr = "XXXXX@gmail.com" #add here recipient's e-mail address
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Alert: Broadcast Date Anniversary!"
            body = 'Broadcast Date Anniversary in one of the Sound Archive collections: ID number: ' + ckey + 'Item title: '+ title + '. Programme Title: ' + programme_title + '. Anniversary: ' + anniversary_year + 'years. Duration:  ' + duration +' Collection name: ' + collection_name + '. Curatorial area: ' + curatorial_area + '.' 
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "XXXXXXX") #replace Xs with e-mail password
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()


import csv
with open('C:\\Users\\lcavo\\Desktop\\Implementation\\Output_Radio.csv', newline='', encoding="ISO-8859-1") as csvfile:
    reader = csv.DictReader(csvfile) 
    for row in reader:
        if row['is_full_anniversary_broadcast']=='TRUE':
            title= row['246']
            ckey= row['id']
            duration=row['301']
            collection_name=row["490"]
            programme_title=row["474"]
            curatorial_area=row["$<icat1:3>"]
            anniversary_year = row['anniversary_year']
            print('sending email with Title: ' + title + '' + ckey)
            send_email()
    

