import os
import shutil
import pygit2
import json
import requests

def create_commit(repo, username):
    #add all files to staging area
    index = repo.index
    index.add_all()
    index.write()

    #create a new tree empty tree object
    author = pygit2.Signature(username + ' Author', username + '@authors.tld')
    commiter = pygit2.Signature(username + ' Committer', username + '@committers.tld')
    tree = index.write_tree()

    #create a new commit in a new branch
    repo.create_commit(
        'refs/heads/new',
        author,
        commiter,
        'Init Commit',
        tree,
        []
    )

    #change the HEAD to new branch
    repo.checkout('refs/heads/new')

#clone git repo and initialize submodules
def clone(url, path, username, password):
    clone_repo = pygit2.clone_repository(
        url, 
        path, 
        callbacks = pygit2.RemoteCallbacks(
                pygit2.UserPass(
                    username, 
                    password
                )
            )
    )
    clone_repo.init_submodules()
    clone_repo.update_submodules()
    return clone_repo

#delete all the git repo history
def delete_history(repo_path, repo, username, output_repo_name):

    #delete README.md
    if(os.path.exists(os.path.join(repo_path, 'README.md'))):
        os.remove(os.path.join(repo_path, 'README.md'))

    #delete License.txt
    if(os.path.exists(os.path.join(repo_path, 'LICENSE'))):
        os.remove(os.path.join(repo_path, 'LICENSE'))

    create_commit(repo, username)

    #delete all other branches
    for b in repo.branches.local:
        if(b != 'new'):
            repo.branches.delete(b)

    #rename new branch to main
    repo.branches['new'].rename('main')

    #delete all remotes
    n = len(repo.remotes)-1
    for r in range(0, len(repo.remotes)):
        repo.remotes.delete(repo.remotes[n].name)
        n -= 1

    #create a new remote origin
    repo.remotes.create(
        'origin', 
        'https://github.com/' + username + '/' + output_repo_name
    )

def new_github_repo(username, password, repo_name):
    response = requests.post(
        url = 'https://api.github.com/user/repos', 
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }, 
        data = json.dumps({
            'name': repo_name
        }), 
        auth = (username, password)
    )
    
    if(response.status_code == 201):
        return True
    else:
        return False

def push_repo(repo, username, password, github_repo_name):
    try:
        repo.remotes['origin'].push(
            ['refs/heads/main'],
            pygit2.RemoteCallbacks(
                pygit2.UserPass(
                    username, 
                    password
                )
            )
        )

        return True
    except Exception as e:
        requests.delete(
            url = 'https://api.github.com/repos/' + username + '/' + github_repo_name,
            headers = {
            'Accept': 'application/vnd.github.v3+json'
            },
            auth = (username, password)
        )
        return False
        