import glob
import os      # for getting just the name of the file
import re
import json

current_directory = './' # directory to search for files

def main():
    filenames = collect_csv_files(current_directory)
    student_data = cat_data(filenames)
    write_csv(student_data)
    write_json(student_data)


def collect_csv_files(dir):
    '''
    gets all the csv files in ./$dir
    '''
    return glob.glob(dir + '*.csv')



def get_file_contents(filename):
    '''
    given path to file, returns contents minus whitespace, empty lines and comments (#)
    '''
    with open(filename) as f:
        cleaned_file = '' # to store cleaned up version of file
        for line in f:
            ls = line.strip() # remove whitespace

            # if line does not start with '#' and is still not empty, keep it
            if not ls.startswith('#') and ls: 
                cleaned_file += ls

        return cleaned_file


def cat_data(filenames):
    '''
    concatenates file contents into a dictionary keyed by netID
    '''

    student_data = {} # will eventually contain all the csv student data
    num_camel_case = 0
    unique_teams = []

    for fn in filenames:
        # get name of file without extension or directory
        name = os.path.basename(fn).rsplit('.', 1)[0]

        # confirm that name is valid
        if(name != 'mlp6' and name != 'everyone'):
            netID = name.lower()

            single_student_data = get_file_contents(fn)
            team_name = single_student_data.split(',')[-1].strip() # extract team name
            
            # check if the team name is valid
            if(not check_no_spaces(team_name)):
                print('Invalid Team Name: ' + team_name)
                exit(0)

            # keep track of unique team names
            if(team_name not in unique_teams):
                unique_teams.append(team_name)

                # keep track of how many unique team names are in camel case
                if(is_camel_case(team_name)):
                    num_camel_case += 1        
        
            student_data[netID] = single_student_data
    
    print('Number of team names using CamelCase: {}'.format(num_camel_case))
    return student_data


def check_no_spaces(string):
    '''
    returns True if @string has no spaces (internal)
    '''
    return ' ' not in string.strip()


def is_camel_case(string):
    '''
    returns True if @string is in CamelCase
    '''
    # split the string at capital letters only
    # regex derived from https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters
    camel_humps = re.findall('[A-Z][^A-Z]*', string.strip())
    for hump in camel_humps:
        camel_case = hump[0].isupper() and hump[1:].islower()
        if(not camel_case):
            return False
    return True



def write_csv(student_data):
    '''
    writes a single csv given array of entries
    '''
    with open('everyone.csv', 'w') as f:
        f.write('\n'.join(student_data.values()))


def write_json(student_data):
    '''
    writes a single json per student
    '''
    for netID, data in student_data.items():
        allData = [item.strip() for item in data.split(',')]

        # dict containing student data
        student_json = {
            'FirstName': allData[0],
            'LastName': allData[1],
            'NetID': allData[2],
            'Github': allData[3],
            'TeamName': allData[4],
        }

        json_version = json.dumps(student_json, sort_keys=False) # convert dict to json
        json_file_path = '{}{}.json'.format(current_directory, netID) # get file path for student data

        # write to file
        with open(json_file_path, 'w') as f:
            f.write(json_version)

if __name__ == "__main__":
    main()
