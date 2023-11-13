import requests
import json
import inspect


repos_in_workspace = []
projects_in_workspace = []

check_branching_model = []
check_branch_restrictions = []
updated_repos = []

def get_main_branch():
    for repo in repos_in_workspace:
        repo_name = repo['slug']
        repo_main_branch = repo['mainbranch']['name']
        if repo_main_branch != "develop":
            print(f'[{inspect.stack()[0][3]}] The repo {repo_name} is not in accordance with the default main branch.')
            check_branching_model.append(repo)

def set_inheritance_for_repository_settings(repo_name):
    url = f'{base_url}repositories/{workspace}/{repo_name}/refs/branches/develop'
    develop_branch_response = requests.get(url, headers=headers)
    if develop_branch_response.status_code != 200:
        print(f'[{inspect.stack()[0][3]}] branch develop not found in {repo_name}')
        create_develop_branch(repo_name)

    inheritance_url = f'{base_url}repositories/{workspace}/{repo_name}/override-settings'
    payload = json.dumps({
    "default_merge_strategy": True,
    "branching_model": True
    })
    
    headers.update({'Content-Type': 'application/json'})
    inheritance_response = requests.request("PUT", inheritance_url, headers=headers, data=payload)

    if inheritance_response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error setting inheritance for repository settings for {repo_name}')

