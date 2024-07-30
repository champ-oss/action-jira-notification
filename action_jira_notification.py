"""Provides functionality to interact with Jira."""

from atlassian import Jira
import os
import logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def jira_auth(host: str, user: str, token: str) -> any:
    """Authenticate to Jira.

    Args:
        host: Jira host.
        user: Jira username.
        token: Jira token.
    """
    return Jira(url='https://' + host, username=user, password=token, cloud=True)


def check_existing_issue(jira: str, project: str, repo: str, workflow_name: str) -> any:
    """Check existing issue on Jira.

    Args:
        jira: Jira object.
        project: Jira project.
        repo: Repository name.
        workflow_name: Workflow name.
    """
    jql_request = (
        'project = ' + project + ' AND labels = ' + repo + ' AND labels = ' + workflow_name +
        ' AND (status != Done AND status != Resolved)'
    )

    jira_data = jira.jql(jql_request)
    return jira_data['total'], jira_data['issues']


def get_description(repo: str, workflow_name: str) -> str:
    """Generate description.

    Args:
        repo: Repository name.
        workflow_name: Workflow name.
    """
    github_server_url = os.environ.get('GITHUB_SERVER_URL', 'https://github.com')
    github_repo = os.environ.get('GITHUB_REPOSITORY')
    github_run_id = os.environ.get('GITHUB_RUN_ID')
    return (
        'Job Info: ' + repo + ' - ' + workflow_name + ' failure\n'
        + f'workflow failure URL: {github_server_url}/{github_repo}/actions/runs/{github_run_id}\n'
        'Please check the job logs for more information.\n'
    )


def create_jira_issue(jira: str, project: str, repo: str, workflow_name: str, jira_type: str) -> any:
    """Create issue on Jira.

    Args:
        jira: Jira object.
        project: Jira project.
        repo: Repository name.
        workflow_name: Workflow name.
        jira_type: Jira issue type.
    """
    issue_dict = {
        'project': {'key': project},
        'summary': repo + ' - ' + workflow_name + ' failure',
        'description': get_description(repo, workflow_name),
        'issuetype': {'name': jira_type},
        'labels': [repo, workflow_name]
    }
    jira.issue_create(fields=issue_dict)


def close_jira_issue(jira: str, issue_id: str) -> any:
    """Close issue on Jira.

    Args:
        jira: Jira object.
        issue_id: Jira issue id.
    """
    jira.issue_transition(issue_id, 'Resolved')


def main() -> None:
    """
    Handle the main execution of the action workflow.

    :return: None
    """
    repo = os.environ.get('GITHUB_REPOSITORY').split('/')[1]
    jira_project = os.environ.get('JIRA_PROJECT')
    jira_token = os.environ.get('JIRA_TOKEN')
    jira_host = os.environ.get('JIRA_HOST')
    jira_user = os.environ.get('JIRA_USER')
    jira_type = os.environ.get('JIRA_TYPE', 'Incident')
    github_wf_name = (os.environ.get('CUSTOM_WORKFLOW_NAME') + '-job-type', os.environ.get('GITHUB_WORKFLOW') + '-job'
                                                                                                                '-type')
    github_wf_name_suffix = github_wf_name if github_wf_name[0] is not None else github_wf_name[1]

    get_jira_auth = jira_auth(jira_host, jira_user, jira_token)
    get_issue_count, get_jira = check_existing_issue(get_jira_auth, jira_project, repo, github_wf_name_suffix)

    if get_issue_count == 0 and os.environ.get('GITHUB_JOB_STATUS') == 'failure':
        logger.info('creating new issue on jira')
        create_jira_issue(get_jira_auth, jira_project, repo, github_wf_name_suffix, jira_type)
    elif get_issue_count > 0 and os.environ.get('GITHUB_JOB_STATUS') == 'success':
        for issue in get_jira:
            logger.info('closing issue on jira')
            close_jira_issue(get_jira_auth, issue['key'])


if __name__ == '__main__':
    main()
