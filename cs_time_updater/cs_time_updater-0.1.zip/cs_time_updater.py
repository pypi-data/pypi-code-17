"""
__author__ mbranche
this is a script to update user time limits, and reservation maxes on Quali Cloudshell

"""
import time
import json
import csv
import pymssql as mdb

######################################################
# Aux Functions

# import json config file
def import_json_config():
    global configs
    json_file_path = 'config.json'
    configs = json.loads(open(json_file_path).read())

# logging function
def write2log(logfile, entry):
    f=open(logfile, 'a')
    temp = ''
    temp += time.strftime('%Y-%m-%d %H:%M:%S')
    temp += ' || '
    temp += entry
    temp += '\n'
    f.write(temp)
    f.close()

# list comparision
def check_list(list, item):
    # returns true if the item is in the list
    try:
        index = list.index(item)
        return True
    except:
        return False

# check username against Database
def check_username(cs_session,username):
    user = cs_session.UserInfo.Name
    # set username in system variable
    if user == True:
        username_ok = True
    else:
        username_ok = False
    return username_ok

# Update username reservation max, and time limit
def update_database(username, time_limit, reservation_max):
    # Connect to Database, this is information is currently filled manually, but can use the json.config
    database = mdb.connect("172.16.59.48", "saqualsys", "qu4lSYS!4u", "Quali_Clone3")

    # server="172.16.59.48", port=1433, user="saqualsys", passwd="qu4lSYS!4u", database="Quali_Clone3"
    # configs["sql_qs_server_hostname"], configs["sql_qs_server_port"],configs["sql_qs_server_username"], configs["sql_qs_server_password"],configs["sql_qs_server_database"])

    # Make an executing object for that database
    cur = database.cursor()

    # Put the SQL code into a string to be passed in
    dbStatement_res = "UPDATE [Quali].[dbo].[UserInfo] SET MaxConcurrentReservations = %i WHERE Username = '%s';" % (int(reservation_max), username)
    a = int(len(time_limit))
    minutes = 0
    if a == 1 or a == 2:
        minutes = int(time_limit) * 60
    if a >= 3:
        temp = int(time_limit) / 100
        minutes = int(temp * 60 * 24)
    dbStatement_time = "UPDATE [Quali].[dbo].[UserInfo] SET MaxReservationDuration = %i WHERE Username = '%s';" % (int(minutes), username)

    print dbStatement_res
    print dbStatement_time

    # Execute the SQL statements
    cur.execute(dbStatement_res)
    cur.execute(dbStatement_time)

    # Close the socket
    database.close()

#################################################################################
# Main Function

def main():
    # grabs config file
    import_json_config()
    # initialize CloudShell API Session
    # cs_session = cs_api.CloudShellAPISession(configs["qs_server_hostname"], configs["qs_admin_username"], configs["qs_admin_password"], configs["qs_admin_domain"])

    # Start log
    write2log(configs["log_file_path"],'---=== * Starting Time Limit and Reservation Max Run * ===---')

    # set csv master list
    master_list_name = configs["time_limit_path"]
    display_name = []
    username = []
    email = []
    time_limit = []
    reservation_max = []
    username_not_in_system = []


    # assign user info to arrays
    write2log(configs["log_file_path"],'-- Running user list creation subroutine')
    file = open(master_list_name, "r")
    worksheet = csv.reader(file, delimiter=',', quotechar='|')
    for row in worksheet:
        a = row
        display_name.append(a[0])
        username.append(a[1])
        email.append(a[2])
        time_limit.append(a[3])
        reservation_max.append(a[4])

    # eliminate headers
    display_name.pop(0)
    username.pop(0)
    email.pop(0)
    time_limit.pop(0)
    reservation_max.pop(0)

    # walk and update usernames
    write2log(configs["log_file_path"], '-- Running user check and update subroutine')
    e = 0
    for i in username:
        # if using white list see if they are on it
        if configs["qs_use_whitelist"] == 1:
            wl_check = check_list(configs["qs_whitelist"], username[e])
        else:
            wl_check = False

        # if whitelist - ignore active status (don't do anything)
        if wl_check:
            write2log(configs["log_file_path"], '-- user passed: ' + username[e])
            pass
        else:
            # if username is in database, and not on white list update
            print 'setting user: %s, time: %s, reservation max: %s' % (username[e], time_limit[e], reservation_max[e])
            update_database(username[e], time_limit[e], reservation_max[e])
            write2log(configs["log_file_path"], '-- user updated: ' + username[e] + ', time limit: ' + time_limit[e] + ', res_max: ' + reservation_max[e])
        e += 1

    write2log(configs["log_file_path"], '>> COMPLETE <<')

################################################################

if __name__ == '__main__':
    main()
