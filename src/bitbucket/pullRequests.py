import requests
import inspect
from config import base_url, workspace, headers

# Add a user to the default reviewers
def add_a_user_to_the_default_reviewers(repo_slug, target_username):
    url = f'{base_url}repositories/{workspace}/{repo_slug}/default-reviewers/{target_username}'
    payload = ""

    headers.update({'Accept': 'application/json'})
    response = requests.put(url, headers=headers, data=payload)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error adding reviewer {target_username} to repo {repo_slug}')
    else:
        print(f'[{inspect.stack()[0][3]}] Reviewer {target_username} added to repo {repo_slug}')

# Remove a user from the default reviewers
def remove_a_user_from_the_default_reviewers(repo_name, target_username):
    url = f'{base_url}repositories/{workspace}/{repo_name}/default-reviewers/{target_username}'

    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error removing reviewer {target_username} from repo {repo_name}')
    else:
        print(f'[{inspect.stack()[0][3]}] Reviewer {target_username} removed from repo {repo_name}')
