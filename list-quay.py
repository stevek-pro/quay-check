#!/usr/bin/env python3
# __author__ = Stephan Kristyn <steve@stevek.pro> & Marcel Oed <marcel@ventx.de> 

import requests
from pprint import pprint
import json
from argparse import ArgumentParser
from sys import exit

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(args):

    quay_token = '<YOUR TOKEN>'
    namespace = '<YOUR CUSTOMER NAMESPACE>'
    header = {
        'Authorization': 'Bearer ' + quay_token
    }

    url = 'https://quay.io/api/v1/repository'

    params = {
        'public': False,
        'namespace': namespace
    }

    # Fetch available Repositorys
    myResponse = requests.get(url, headers=header, params=params)
    quay_repositories = set()

    if(myResponse.ok):

        jData = json.loads(myResponse.content)
        for entity in jData["repositories"]:
            if entity["kind"] == "image":
                quay_repositories.add(entity["name"])
    else:
        myResponse.raise_for_status()
 
    # Do we limit our lookup on one repository?
    if args.repo != None:
        if args.repo in quay_repositories:
            quay_repositories = set()
            quay_repositories.add(args.repo)
        else:
            print(bcolors.BOLD + bcolors.FAIL + '\n\tERROR: Repository %s not found!\n' % args.repo + bcolors.ENDC )
            exit(1)

    # do we exclude repos ? 
    if args.exclude != None:
        exclude_list = [x.strip() for x in args.exclude.split(",")]
        quay_repositories = quay_repositories.difference(exclude_list)
        
    # Get build state
    state = dict()
    quay_repositories = sorted(quay_repositories)
    for repo in quay_repositories:
        state[repo] = []
        url = 'https://quay.io/api/v1/repository/' + namespace + '/' + repo + '/build/'

        params = {
           'limit': '25'
        }
        myResponse = requests.get(url, headers=header, params=params)
        if(myResponse.ok):
            jData = json.loads(myResponse.content)
            for build in jData['builds']:
                if args.tag in build["tags"]:
                    state[repo].append({
                        'id': build['id'],
                        'phase': build['phase'],
                        'started': build['started'],
                        'tags': build['tags'],
                        'commit': build['trigger_metadata']['commit'],
                        'message': build['trigger_metadata']['commit_info']['message'],
                    })
        else:
            myResponse.raise_for_status()

    # Outputs
    for repo in quay_repositories:
        print('Service: ' + bcolors.ENDC + bcolors.BOLD + bcolors.OKBLUE + repo + bcolors.ENDC)
        print('\t' + bcolors.HEADER + bcolors.UNDERLINE + \
        'Build Start\t\t\t' + 'Tags\t\t' + 'Phase' + bcolors.ENDC)
        for build in state[repo]:
            align_buffer = " " * ( 16 - len(", ".join(build['tags'])) )
            if build['phase'] == 'error':
                state_color = bcolors.FAIL + bcolors.BOLD
            elif build['phase'] == 'complete':
                state_color = bcolors.OKGREEN
            else:
                state_color = bcolors.WARNING
            print('\t' + build['started'] + '\t' + ", ".join(build['tags']) + \
                    align_buffer + state_color + build['phase'] + bcolors.ENDC)
        if not state[repo]:
            print(bcolors.FAIL + bcolors.BOLD + '\tNOTHING FOUND\t\t\t-\t\terror' + bcolors.ENDC)
        print('')


if __name__ == "__main__":
    parser = ArgumentParser(description='Script for verifing the presence of Docker builds for certain tags in Quay.')
    requiredNamed = parser.add_argument_group('required arguments')

    # required arguments
    requiredNamed.add_argument('-t', '--tag', metavar='TAG', \
                               help='Lookup for certain build tag', required=True)
    
    # optional arguments
    parser.add_argument('-r', '--repo', metavar='SAVEUP-EXAMPLE', \
                                help="Limit lookup to one repository")

    parser.add_argument('-e', '--exclude', metavar='repo1,repo2', \
                                help="Exclude specified repositories")
    args = parser.parse_args()
    main(args)