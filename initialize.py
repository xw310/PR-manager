#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
initialization target:
1.Create necessary labels before running main.py
2.Add labels to corresponding pull request before running main.py
'''

import time
from github_api import *
from util import *

def create_label_init():
    '''
    create labels before running PR_helper for the first time
    '''
    print('enter create_label_init\n')
    # creat two new labels
    # need to judge if some labels already created in the last initialization \
    # otherswise leading to 422
    all_labels = get_all_labels()
    target_label = get_target_label(all_labels)
    print('target labels found: {}\n'.format(target_label))

    if TWO_WEEK_LABEL['NAME'] in target_label:
        print('{} label found\n'.format(TWO_WEEK_LABEL['NAME']))
    else:
        print('{} label not found, begin creating it...'.format(TWO_WEEK_LABEL['NAME']))
        create_new_label(TWO_WEEK_LABEL['NAME'], TWO_WEEK_LABEL['DESCRIPTION'], TWO_WEEK_LABEL['COLOR'])
        print('{} label created\n'.format(TWO_WEEK_LABEL['NAME']))

    if THREE_WEEK_LABEL['NAME'] in target_label:
        print('{} label found\n'.format(THREE_WEEK_LABEL['NAME']))
    else:
        print('{} label not found, begin creating it...'.format(THREE_WEEK_LABEL['NAME']))
        create_new_label(THREE_WEEK_LABEL['NAME'], THREE_WEEK_LABEL['DESCRIPTION'], THREE_WEEK_LABEL['COLOR'])
        print('{} label created\n'.format(THREE_WEEK_LABEL['NAME']))

    if IGNORE_LABEL['NAME'] in target_label:
        print('{} label found\n'.format(IGNORE_LABEL['NAME']))
    else:
        print('{} label not found, begin creating it...'.format(IGNORE_LABEL['NAME']))
        create_new_label(IGNORE_LABEL['NAME'], IGNORE_LABEL['DESCRIPTION'], IGNORE_LABEL['COLOR'])
        print('{} label created\n'.format(IGNORE_LABEL['NAME']))

    print('create_label_init succeed\n\n')


def add_labels_init():
    '''
    add labels before running PR_helper for the first time
    '''
    print('enter add_labels_init\n')
    # get issues and initial labels/comments for issues
    all_issues = get_all_issues()
    #
    for issue in all_issues:
        if 'pull_request' in issue:
            create_time= issue['created_at']
            issue_number = issue['number']
            issue_title = issue['title']
            html_url = issue['html_url']
            print('processing pull request {}, which is created at {}'.format(issue_number, create_time))

            #check time
            duration_in_day = calculate_pr_duration(create_time)
            #check label
            labels = issue['labels']
            target_label = get_target_label(labels)
            print('duration of this pull request is: {} days'.format(duration_in_day))
            print('target label of this pull request: {}'.format(target_label))

            if duration_in_day < DURATION_MAP['TWO_WEEK']:
                print('no need to add label\n')
                pass
            elif duration_in_day < DURATION_MAP['THREE_WEEK']:
                # add two_weeks_already label
                add_label_to_issue(TWO_WEEK_LABEL['NAME'], issue_number)
                add_comment_to_issue(TWO_WEEK_LABEL['COMMENT_TEMPLATE'], issue_number, issue_title, html_url)
                print('add {} label successfully\n'.format(TWO_WEEK_LABEL['NAME']))
            else:
                if TWO_WEEK_LABEL['NAME'] in target_label:
                    delete_label_from_issue(TWO_WEEK_LABEL['NAME'], issue_number)
                # add three_weeks_already label
                add_label_to_issue(THREE_WEEK_LABEL['NAME'], issue_number)
                if IGNORE_LABEL['NAME'] in target_label:
                    add_comment_to_issue(THREE_WEEK_LABEL['COMMENT_TEMPLATE_UNDER_IGONRE'], issue_number, issue_title, html_url)
                else:
                    add_comment_to_issue(THREE_WEEK_LABEL['COMMENT_TEMPLATE'], issue_number, issue_title, html_url)
                print('add {} label successfully\n'.format(THREE_WEEK_LABEL['NAME']))

    print('add_labels_init succeed\n\n')


def initialize():
    '''
    including create_label_init and add_labels_init
    '''
    create_label_init()
    add_labels_init()


################
if __name__ == '__main__':
    initialize()
