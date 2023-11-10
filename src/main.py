import os
import requests
import json
from dotenv import load_dotenv
import inspect

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
workspace = os.getenv('WORKSPACE')
defaultReviewers = os.getenv('DEFAULT_REVIEWERS').split(',')
min_date = os.getenv('MIN_DATE')

base_url = "https://api.bitbucket.org/2.0/"
headers = {
  'Authorization': f'Basic {password}'
}

repos_in_workspace = []
projects_in_workspace = []

check_branching_model = []
check_branch_restrictions = []
updated_repos = []

def list_projects_in_workspace():
    url = f'{base_url}workspaces/{workspace}/projects'
    response = requests.get(url, headers=headers)
    data = response.json()
    projects_in_workspace.extend(data['values'])

    print(f'[{inspect.stack()[0][3]}] {projects_in_workspace.__len__()} projects found')

def list_repos_in_workspace():
    url = f'{base_url}repositories/{workspace}'
    response = requests.get(url, headers=headers)
    repos_in_workspace.extend(response.json().get('values', []))

    while True:
        response = requests.get(url, headers=headers)
        repos_in_workspace.extend(response.json().get('values', []))
        next_url = response.json().get('next')
        if next_url is None:
            break
        url = next_url

    print(f'[{inspect.stack()[0][3]}] {repos_in_workspace.__len__()} repos found')
    return repos_in_workspace

def get_branching_model_for_project():
    for repo in repos_in_workspace:
        repo_name = repo['slug']
        url = f'{base_url}workspaces/{workspace}/projects/{repo["project"]["key"]}/branching-model'
        branching_model_response = requests.get(url, headers=headers)
        branching_model_data = branching_model_response.json()

        development_branch = branching_model_data['development']['name']
        production_branch = branching_model_data['production']['name']

        if development_branch != "develop" or production_branch != "master":
            print("[{inspect.stack()[0][3]}] The repo " + repo_name + " is not in accordance with the default branching model.")
            check_branching_model.append(repo)

def check_and_set_branching_model_for_repo():
    for repo in repos_in_workspace:
        repo_name = repo['slug']
        url = f'{base_url}repositories/{workspace}/{repo_name}/branching-model'
        branching_model_response = requests.get(url, headers=headers)
        branching_model_data = branching_model_response.json()

        if 'development' not in branching_model_data:
            print(f'[{inspect.stack()[0][3]}] Repo {repo_name} "development" not in branching_model_data')
            set_inheritance_for_repository_settings(repo_name)

        if 'production' not in branching_model_data:
            print(f'[{inspect.stack()[0][3]}] Repo {repo_name} "production" not in branching_model_data')
            set_inheritance_for_repository_settings(repo_name)

        if 'development' not in branching_model_data or 'production' not in branching_model_data:
            continue

        development_branch = branching_model_data['development']['name']
        production_branch = branching_model_data['production']['name']

        if development_branch != "develop" or production_branch != "master":
            print(f'[{inspect.stack()[0][3]}] Repo {repo}: development_branch != "develop" or production_branch != "master"')
            
        set_inheritance_for_repository_settings(repo_name)

def get_branch_restrictions():
    for repo in repos_in_workspace:
        repo_name = repo['slug']
        url = f'{base_url}repositories/{workspace}/{repo_name}/branch-restrictions'
        branch_restrictions_response = requests.get(url, headers=headers)
        branch_restrictions_data = branch_restrictions_response.json()

        if branch_restrictions_data['values'] != None:
            print(f'[{inspect.stack()[0][3]}] The repo {repo_name} is not in accordance with the default branch restrictions.')
            check_branch_restrictions.append(repo)

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

def create_develop_branch(repo_name):
    url = f'{base_url}repositories/{workspace}/{repo_name}/refs/branches/master'
    master_branch_response = requests.get(url, headers=headers)

    if master_branch_response.status_code != 200:
        print(f'[{inspect.stack()[0][3]}] branch master not found in {repo_name}')
        return
    
    master_branch_data = master_branch_response.json()

    url = f'{base_url}repositories/{workspace}/{repo_name}/refs/branches'
    target_content = master_branch_data['target']
    payload = json.dumps({
    "type": "branch",
    "name": "develop",
    "default_merge_strategy": "merge_commit",
    "target": target_content
    })

    branch_response = requests.request("POST", url, headers=headers, data=payload)

    if branch_response.status_code != 201:
        print(f'[{inspect.stack()[0][3]}] Error creating develop branch for {repo_name}')

def list_updated_repositories():
    for repo in repos_in_workspace:
        repo_updated_on = repo['updated_on']
        
        if repo_updated_on > min_date:
            updated_repos.append(repo['slug'])

    return updated_repos

def set_default_reviewers_by_repo(repo_name):
    url = f'{base_url}repositories/{workspace}/{repo_name}/default-reviewers/'
    payload = ""

    for reviewer in defaultReviewers:
        url = f'{url}{reviewer}'
        set_reviewer_response = requests.request("PUT", url, headers=headers, data=payload)
        if set_reviewer_response.status_code != 200:
            print(f'[{inspect.stack()[0][3]}] Error setting reviewer {reviewer} for repo {repo_name}')

def delete_default_reviewers_by_repo(repo_name):
    url = f'{base_url}repositories/{workspace}/{repo_name}/default-reviewers/'

    for reviewer in defaultReviewers:
        url = f'{url}{reviewer}'
        response = requests.delete(url, headers=headers)
        if response.status_code != 204:
            print(f'[{inspect.stack()[0][3]}] Error deleting reviewer {reviewer} from repo {repo_name}')
        else:
            print(f'[{inspect.stack()[0][3]}] Reviewer {reviewer} deleted from repo {repo_name}')

def set_default_reviewers_by_project(project_key):
    url = f'{base_url}workspaces/{workspace}/projects/{project_key}/default-reviewers'
    payload = ""

    for reviewer in defaultReviewers:
        url = f'{url}/{reviewer}'
        set_reviewer_response = requests.request("PUT", url, headers=headers, data=payload)
        if set_reviewer_response.status_code != 200:
            print(f'[{inspect.stack()[0][3]}] Error setting reviewer {reviewer} for project {project_key}')

def list_repos_with_updated_commit():
    for repos in repos_in_workspace:
        repo_name = repos['slug']
        set_default_reviewers_by_repo(repo_name)
        list_group_permissions(repo_name)
        list_user_permissions(repo_name)
        updated_commit_date = ''
        url = f'{base_url}repositories/{workspace}/{repo_name}/refs'
        branch_list_response = requests.get(url, headers=headers)
        branch_list_data = branch_list_response.json()
        values = branch_list_data['values']

        updated_commit_date = ''
        for value in values:
            commit_date = value['target']['date']
            if updated_commit_date == '':
                updated_commit_date = commit_date
            
            if commit_date > updated_commit_date:
                updated_commit_date = commit_date

        if updated_commit_date >= min_date:
            updated_repos.append(repos['slug'])
            print(f'[{inspect.stack()[0][3]}] Repo updated after {min_date}: {repo_name}')

    file = f"updated_repos_{min_date}.json"

    with open(file, 'w') as f:
        json.dump(updated_repos, f)
        print(f'[{inspect.stack()[0][3]}] {updated_repos.__len__()} repos updated after {min_date} saved in {file}')

def delete_user_permissions(repo_name, user_id):
    url = f'{base_url}repositories/{workspace}/{repo_name}/permissions-config/users/{user_id}'
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error deleting user {user_id} from repo {repo_name}')
    else:
        print(f'[{inspect.stack()[0][3]}] User {user_id} deleted from repo {repo_name}')

def list_user_permissions(repo_name):
    url = f'{base_url}repositories/{workspace}/{repo_name}/permissions-config/users'
    response = requests.get(url, headers=headers)
    data = response.json()
    values = data['values']

    for value in values:
        delete_user_permissions(repo_name, value['user']['uuid'])

def delete_group_permissions(repo_name, group_slug):
    url = f'{base_url}repositories/{workspace}/{repo_name}/permissions-config/groups/{group_slug}'
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        print(f'[{inspect.stack()[0][3]}] Error deleting group {group_slug} from repo {repo_name}')
    else:
        print(f'[{inspect.stack()[0][3]}] Group {group_slug} deleted from repo {repo_name}')

def list_group_permissions(repo_name):
    url = f'{base_url}repositories/{workspace}/{repo_name}/permissions-config/groups'
    response = requests.get(url, headers=headers)
    data = response.json()
    values = data['values']

    for value in values:
        delete_group_permissions(repo_name, value['group']['slug'])
