#!/usr/bin/python3
# usage: python action-jira-notification.py
# export JIRA_TOKEN, JIRA_HOST, JIRA_PROJECT, JIRA_USER, JIRA_TYPE as env variable
#########################################################################################################
# coding=utf-8
from atlassian import Jira
import os


def jira_auth(host: str, user: str, token: str) -> any:
    # jira auth requirements
    jira = Jira(
        url="https://" + host,
        username=user,
        password=token,
        cloud=True)
    return jira


def check_existing_issue(jira: str, project: str, repo: str, workflow_name: str) -> any:
    # default jira JQL query string
    jql = ("project = " + project + " AND labels = " + repo + " AND labels = " + workflow_name +
           " AND (status != 'Done' AND status != 'Resolved')")

    data = jira.jql(jql)
    # checking json total value
    get_total_issue_count = data['total']
    get_jira_issue_ids = data['issues']
    return get_total_issue_count, get_jira_issue_ids


def get_description(repo: str, workflow_name: str) -> str:
    """Generate description. """
    github_server_url = os.environ.get('GITHUB_SERVER_URL', 'https://github.com')
    github_repo = os.environ.get('GITHUB_REPOSITORY')
    github_run_id = os.environ.get('GITHUB_RUN_ID')
    return (
        repo + ' - ' + workflow_name + ' failure\n'
        + f'workflow failure URL: {github_server_url}/{github_repo}/actions/runs/{github_run_id}\n'
    )


def create_jira_issue(jira: str, project: str, repo: str, workflow_name: str, jira_type: str) -> any:
    issue_dict = {
        'project': {'key': project},
        'summary': repo + " - " + workflow_name + " failure",
        'description': get_description(repo, workflow_name),
        'issuetype': {'name': jira_type},
        'labels': [repo, workflow_name]
    }
    jira.issue_create(fields=issue_dict)


def close_jira_issue(jira: str, issue_id: str) -> any:
    jira.issue_transition(issue_id, 'Done', comment='Closing issue as workflow was successful')


def main():
    repo = os.environ.get('GITHUB_REPOSITORY').split('/')[1]
    jira_project = os.environ.get('JIRA_PROJECT')
    jira_token = os.environ.get('JIRA_TOKEN')
    jira_host = os.environ.get('JIRA_HOST')
    jira_user = os.environ.get('JIRA_USER')
    jira_type = os.environ.get('JIRA_TYPE', 'Incident')
    github_wf_name = os.environ.get('GITHUB_WORKFLOW')
    github_wf_name_suffix = github_wf_name + '-job_type'

    get_jira_auth = jira_auth(jira_host, jira_user, jira_token)
    get_issue_count, get_jira = check_existing_issue(get_jira_auth, jira_project, repo, github_wf_name_suffix)
    if get_issue_count == 0 and os.environ.get('GITHUB_JOB_STATUS') == 'failure':
        print('creating issue on jira as workflow failed')
        create_jira_issue(get_jira_auth, jira_project, repo, github_wf_name_suffix, jira_type)
    elif get_issue_count > 0 and os.environ.get('GITHUB_JOB_STATUS') == 'success':
        for issue in get_jira:
            print('closing existing issues on jira as workflow was successful')
            close_jira_issue(get_jira_auth, issue['key'])
    else:
        print('not creating issue or closing issue')


main()
