import inspect
import json
from config import defaultBranches, min_date
from bitbucket.refs import list_branches_and_tags, create_a_branch

def list_repos_with_updated_commit(repos_in_workspace):
    updated_repos = []
    for repos in repos_in_workspace:
        repo_slug = repos['slug']
        last_commit_date = ''
        branches = list_branches_and_tags(repo_slug)

        for branch in branches:
            commit_date = branch['target']['date']
            if last_commit_date == '':
                last_commit_date = commit_date
            
            if commit_date > last_commit_date:
                last_commit_date = commit_date

        if last_commit_date >= min_date:
            updated_repos.append(repos['slug'])
            print(f'[{inspect.stack()[0][3]}] Repo updated after {min_date}: {repo_slug}')

    file = f'updated_repos_{min_date}.json'

    with open(file, 'w') as f:
        json.dump(updated_repos, f)
        print(f'[{inspect.stack()[0][3]}] {updated_repos.__len__()} repos updated after {min_date} saved in {file}')

    return updated_repos

def check_if_default_branches_exists_in_repo(repo_slug):
    default_branches_in_repo = []
    branches_in_repo = list_branches_in_repo(repo_slug)

    for branch in branches_in_repo:
        if branch[0] in defaultBranches:
            default_branches_in_repo.append(branch[0])
    
    if default_branches_in_repo.__len__() == defaultBranches.__len__():
        print(f'[{inspect.stack()[0][3]}] All default branches exists in repo {repo_slug}')
        return True
    else:
        print(f'[{inspect.stack()[0][3]}] Not all default branches exists in repo {repo_slug}')
        return False

def create_default_branches_in_repo(repo_slug, target):
    check = check_if_default_branches_exists_in_repo(repo_slug)
    if check:
        return
    else:
        for branch in defaultBranches:
            create_a_branch(repo_slug, branch, target)

def list_branches_in_repo(repo_slug):
    branches_and_tags_in_repo = list_branches_and_tags(repo_slug)
    branches_in_repo = []

    for item in branches_and_tags_in_repo:
        if item['type'] == 'branch':
            cur_branch = format_branch(item)
            branches_in_repo.append(cur_branch)

    print(f'[{inspect.stack()[0][3]}] {branches_in_repo.__len__()} branches in repo {repo_slug}')
    return branches_in_repo

def format_branch(branch):
    branch_name = branch['name']
    branch_date = branch['target']['date']
    branch_target = branch['target']

    formated_branch = [branch_name, branch_date, branch_target]

    return formated_branch