import requests
import inspect
from config import base_url, workspace, headers

# List repositories in a workspace
def list_repositories_in_a_workspace():
    repos_in_workspace = []
    url = f'{base_url}repositories/{workspace}'
    headers.update({'Accept': 'application/json'})

    while True:
        response = requests.get(url, headers=headers)
        repos_in_workspace.extend(response.json().get('values', []))
        next_url = response.json().get('next')
        if next_url is None:
            break
        url = next_url

    print(f'[{inspect.stack()[0][3]}] {repos_in_workspace.__len__()} repos in workspace {workspace}')
    return repos_in_workspace

# List explicit group permissions for a repository
def list_explicit_group_permissions_for_a_repository(repo_slug):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/permissions-config/groups'

    response = requests.get(url, headers=headers)
    json_data = response.json()

    print(f'[{inspect.stack()[0][3]}] Explicit group permissions for repo {repo_slug}:')
    for group in json_data['values']:
        print(f'[{inspect.stack()[0][3]}] {group}')

# Delete an explicit group permission for a repository
def delete_an_explicit_group_permission_for_a_repository(repo_slug, group_slug):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/permissions-config/groups/{group_slug}'

    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error deleting group {group_slug} from repo {repo_slug}')
    else:
        print(f'[{inspect.stack()[0][3]}] Group {group_slug} deleted from repo {repo_slug}')

# List explicit user permissions for a repository
def list_explicit_user_permissions_for_a_repository(repo_slug):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/permissions-config/users'

    response = requests.get(url, headers=headers)
    json_data = response.json()

    print(f'[{inspect.stack()[0][3]}] Explicit user permissions for repo {repo_slug}:')
    for user in json_data['values']:
        print(f'[{inspect.stack()[0][3]}] {user}')

# Delete an explicit user permission for a repository
def delete_an_explicit_user_permission_for_a_repository(repo_slug, selected_user_id):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id}'

    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error deleting user {selected_user_id} from repo {repo_slug}')
    else:
        print(f'[{inspect.stack()[0][3]}] User {selected_user_id} deleted from repo {repo_slug}')
