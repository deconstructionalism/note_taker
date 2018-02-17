#! /usr/bin/python

'''
OPEN NOTES AND DOCUMENTATION
allows for opening notes markdown file in editor of choice alongside 
documentation in browser

Requirements:
    - 'notes' directory in path of script
    - bash (tested on Darwin Kernel Version 17.3.0)
    - Visual Studio Code in PATH as 'code' (for current EDITOR_ARGS to work)

Settings:
    - SUBJ_BASE_URLS: add new notes subjsects here (subject_name, doc_base_url)
    - NOTES_TEMPLATE: template for new notes files
    - EDITOR_ARGS :   commands to run in order to get editor to recognize 
                      appended file location argument after EDITOR_ARGS
'''
import json
import os
import sys
import webbrowser
from sys import argv
from subprocess import Popen

# for python 2/3 compatibility
try:
    input = raw_input
except NameError:
    pass



SUBJ_BASE_URLS = [
     ('react', 'https://reactjs.org/docs'),
     ('redux', 'https://redux.js.org/docs'),
     ('rxjs', 'http://reactivex.io/rxjs/manual'),
     ('redux-observables', 'https://redux-observable.js.org/docs')
]

NOTES_TEMPLATE = \
'''# {} NOTES

## left off at
---
/'''

# commands to run in order to get editor to recognize appended file location
# argument after EDITOR_ARGS
EDITOR_ARGS = ['code']


def find_notes_dirs(search_dir):
    '''
    Search for dirs containing 'notes.json' files in `search_dir`
    '''
    if not os.path.exists(search_dir):
        print('ERROR: NO SUCH DIRECTORY "{}"'.format(search_dir.upper()))
        return None
    dirs = []
    for directory, _, file_names in os.walk(search_dir):
        if 'notes.json' in file_names:
            notes_path =  os.path.join(directory, 'notes.json')
            with open(notes_path, 'r') as f:
                subjects = json.load(f)
            dir_info = {
                'dir': directory,
                'dir_name': directory.split('/')[-1],
                'subjects': subjects
            }
            dirs.append(dir_info)
    return dirs if len(dirs) > 0 else None


def numerical_menu(enumerable):
    '''
    Allow input selection of integer choice from within range of `enumerable`
    '''
    while True:
        choice = input('?')
        if choice in ['Q', 'q']:
            return None
        try:
            return enumerable[int(choice)]
        except:
            continue

def notes_dirs_menu(dirs):
    print_str = 'CHOOSE NOTES DIRECTORY:'
    print('{}\n{}'.format(print_str, '-' * len(print_str)))
    for i, directory in enumerate(dirs):
       print('{} - {}'.format(i, directory['dir_name']))
    return numerical_menu(dirs)

def subject_menu(directory):
    subjects = directory['subjects']
    print_str = '{} | OPEN NOTES FOR:'.format(directory['dir_name'].upper())
    print('{}\n{}'.format(print_str , '-' * len(print_str)))
    for i, subj in enumerate(subjects):
       print('{} - {}'.format(i, subj['name']))
    return numerical_menu(subjects)


def open_notes(subj, base_url):
    subj = subj.upper()
    base_url = base_url.rstrip('/')
    notes_file = 'notes/{}_notes.md'.format(subj)
    sub_domain = ''
    # if notes file doesn't exist, make from template
    if not os.path.exists(notes_file):
        with open(notes_file, 'w') as f:
            f.write(NOTES_TEMPLATE.format(subj))
    # if notes exists, extract subdomain from last line
    else:
        with open(notes_file, 'r') as f:
            contents = f.read()
            sub_domain = contents.split()[-1].lstrip('/')

    # open full path in web browser
    webbrowser.open_new_tab('{}/{}'.format(base_url, sub_domain))

    # open notes file in editor specified in EDITOR_ARGS
    open_vis_cmd = EDITOR_ARGS + [notes_file]
    Popen(open_vis_cmd)


def main(search_dir='.'):
    # os.system('clear')

    dirs = find_notes_dirs(search_dir)
    if not dirs:
        print('no directories with "notes.json" found in "{}"' \
          .format(search_dir))
        sys.exit(0)

    directory = notes_dirs_menu(dirs) if len(dirs) > 1 else dirs[0]
    if not directory:
        sys.exit(0)

    subject = subject_menu(directory) if len(directory['subjects']) > 1 else directory[0]
    if not subject:
        sys.exit(0)
    
    print subject
    sys.exit(0)

    # print notes options and wait for user response
    print('OPEN NOTES FOR:\n{}'.format('-' * 20))
    for i, subj_tup in enumerate(SUBJ_BASE_URLS):
        subj, base_url = subj_tup
        print('{} - {}'.format(i, subj))
    while True:
        choice = input('?')
        if choice in ['Q', 'q']:
            break
        try:
            subj, base_url = SUBJ_BASE_URLS[int(choice)]
        except:
            continue
        open_notes(subj, base_url)
        break

if __name__ == '__main__':
    search_dir = argv[1] if len(argv) > 1 else '.'
    main(search_dir)
