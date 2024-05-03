"""Provides test for Jira notification."""
from unittest.mock import MagicMock
from action_jira_notification import jira_auth, check_existing_issue, get_description, create_jira_issue, \
    close_jira_issue


def test_jira_auth() -> None:
    """
    When the function is called, it should return a Jira object.

    :return:
    """
    host = 'jira.com'
    user = 'user'
    token = 'token'

    jira = jira_auth(host, user, token)
    assert jira is not None


def test_check_existing_issue_with_existing_issue() -> None:
    """When checking existing issue, it should return the issue count and Jira object.

    :return:
    """
    jira = MagicMock()
    jira.get_issues_list.return_value = [{'key': 'issue_key'}]
    jira_project = 'project'
    repo = 'repo'
    github_wf_name_suffix = 'workflow'

    get_issue_count, get_jira = check_existing_issue(jira, jira_project, repo, github_wf_name_suffix)
    assert get_issue_count is not None
    assert get_jira is not None


def test_check_existing_issue_with_no_existing_issue() -> None:
    """When checking existing issue, it should return the issue count and Jira object.

    :return:
    """
    jira = MagicMock()
    jira.get_issues_list.return_value = []
    jira_project = 'project'
    repo = 'repo'
    github_wf_name_suffix = 'workflow'

    get_issue_count, get_jira = check_existing_issue(jira, jira_project, repo, github_wf_name_suffix)
    assert get_issue_count is not None
    assert get_jira is not None


def test_get_description() -> None:
    """When calling get description, it should return a description.

    :return:
    """
    repo = 'repo'
    workflow_name = 'workflow'

    description = get_description(repo, workflow_name)
    assert description is not None


def test_create_jira_issue() -> None:
    """When creating a Jira issue, it should return a Jira issue.

    :return:
    """
    jira = MagicMock()
    project = 'project'
    repo = 'repo'
    workflow_name = 'workflow'
    jira_type = 'Incident'

    create_jira_issue(jira, project, repo, workflow_name, jira_type)
    assert jira.issue_create.called


def test_close_jira_issue() -> None:
    """When closing a Jira issue, it should return a Jira issue.

    :return:
    """
    jira = MagicMock()
    issue_id = 'issue_id'

    close_jira_issue(jira, issue_id)
    assert jira.issue_transition.called
