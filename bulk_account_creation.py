import os
import shutil
import csv
from arcgis.gis import *

username = #SET USERNAME
password = #SET PASSWORD

print('\nLogging in to AGOL')
gis = GIS(username=username, password=password, verify_cert=False)


user_list = input('Input full file path, including .csv: ').strip('"')
file_name = os.path.basename(user_list)

group_id =' ' #Set Group ID

role_id = ' '  #role code for desired roles

regex = '^[a-z0-9]+[\._-]?[a-z0-9]+@\w+([\.-]?\w+)*(\.(\w{2,3}|online))+$'

def reset_account(user):
    the_user=gis.users.get(user)
    message = """ """  #  Set email message
    email_subject = " " #set email subject
    gis.users.send_notification([user], email_subject, message, type='email')
    the_user.reset(password=None, reset_by_email=True)
    print("Password reset.")

def check_existing(email, user_name):
    print ("Checking "+email+" for existing accounts...")
    queryResults = gis.users.search(query=email, max_users=5)
    if len(queryResults) > 0:
        existing = queryResults[0]
        print("The existing user "+str(existing.username)+" found for email address: " + email)
        print("User "+str(existing.username)+" will be reset")
        reset_account(existing.username)
        return True
    else:
        print ("None found. Creating new user "+user_name+"...")
        return False

def update_bio(user,bio):
    bio_to_update = gis.users.get(user)
    bio_to_update.update(description=bio)
    print("Bio for "+user+" updated")

def email_validator(address):
    print ('Evaluating email '+ address)
    valid_email = address
    while re.search(regex, valid_email) is None:
        print("\n{0} is invalid".format((address)))
        valid_email = input("\nPlease provide correct email: ")
    return valid_email

log_dir = r' '  #set log path
log_list = os.path.join(log_dir, file_name)

toWrite = []

#set up for following CSV template, modify as needed
#first_name,last_name,email,phone,title,organization,county,state

with open(user_list, 'r') as user_list, open(log_list, 'w', newline ='') as log_list:
    reader = csv.reader(user_list)
    writer = csv.writer(log_list)
    i = 0
    for row in reader:
        if i > 0 and len(row[0]) > 0:
            try:
                first_name = row[0]  
                last_name = row[1]
                full_name = row[0] + " " + row[1]
                email = str.lower(row[2])
                phone = row[3]
                title = row[4]
                organization = row[5]
                county= row[6]
                state = row[7]
                user_name = str.lower(first_name[0]) + str.lower(last_name)   #concatenate first initial+last name
                user_name = user_name.replace("'", "").replace("-", "_").replace(" ", "").replace(".","").replace(",","")  #remove special characters
                user_pwds = #set default password
                bio = title + ", " + organization + ", " + county + ", " + state #create bio
                email = email_validator(email)
                create_user = check_existing(email, user_name)  #check for existing user associated with email. Reset password if exists and return True, no user returns false
                if not create_user:
                    new_user = gis.users.create(username=user_name, password=user_pwds, firstname=first_name,lastname=last_name, email=email, role=role_id, user_type='Creator',credits=500, provider = 'arcgis',groups =[group_id])
                    update_bio(user_name,bio)
                    writer.writerow([first_name,last_name,email,user_name])
                    print("User created: "+user_name)
            except Exception as e:
                print(e)
        i = i + 1

print("New users list saved to: " + log_list)

\print("Finished")
