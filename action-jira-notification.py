#!/usr/bin/python3
# usage: python action-jira-notification.py
# export JIRA_TOKEN, JIRA_HOST, JIRA_PROJECT, JIRA_USER, GITHUB_WORKFLOW_NAME and GIT_REPO as env variable
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
    JQL = "project = " + project + " AND labels = " + repo + " AND labels = " + workflow_name + " AND (status = 'To Do' OR status = 'In Progress')"

    data = jira.jql(JQL)
    # checking json total value
    get_total_issue_count = data["total"]

    return get_total_issue_count


def create_jira_issue(jira: str, project: str, repo: str, workflow_name: str, jira_type: str) -> None:
    jira.issue_create(
        fields={
            "project": {
                "key": project
            },
            "labels": [
                repo,
                workflow_name
            ],
            "issuetype": {
                "name": jira_type
            },
            "summary": "" + repo + " failure",
            "description": "" + repo + " - " + workflow_name + " failure",
        }
    )


def main():
    repo = os.environ["GIT_REPO"]
    jiraproject = os.environ["JIRA_PROJECT"]
    jiratoken = os.environ["JIRA_TOKEN"]
    jirahost = os.environ["JIRA_HOST"]
    jirauser = os.environ["JIRA_USER"]
    jira_type = os.environ("JIRA_TYPE")
    github_wf_name = os.environ["GITHUB_WORKFLOW_NAME"]
    # adding suffix as some job types are key words in JQL and can't be used in query
    github_wf_name_suffix = github_wf_name + "-job_type"

    # auth to jira endpoint using host, user and token
    get_jira_auth = jira_auth(jirahost, jirauser, jiratoken)
    # checking if issue exist, creating issue if total count equals zero
    get_issue_count = check_existing_issue(get_jira_auth, jiraproject, repo, github_wf_name_suffix)
    if get_issue_count == 0:
        create_jira_issue(get_jira_auth, jiraproject, repo, github_wf_name_suffix, jira_type)
    else:
        print('not creating issue, already exist........')


main()
