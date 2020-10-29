import os
import shutil
import pygit2

def create_commit(repo, username, email):
    #add all files to staging area
    index = repo.index
    index.add_all()
    index.write()

    #create a new tree empty tree object
    author = pygit2.Signature(username, email)
    commiter = pygit2.Signature(username, email)
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
def clone(url, path):
    clone_repo = pygit2.clone_repository(url, path)
    clone_repo.init_submodules()
    clone_repo.update_submodules()
    return clone_repo

#delete all the git repo history
def delete_history(repo_path, repo, username, email, github_url):

    #delete README.md and LICENSE.txt
    index = repo.index
    
    pygit2.Repository.
    for e in index:
        if e.path == 'README.md': 
            index.remove(os.path.join('./', e.path), repo.)
        # elif e.path == 'LICENSE': 
        #     index.remove(os.path.join(repo_path, e.path + '.txt'))
    
    index.write()
    for e in index:
        print(e.path, e.hex)

    # create_commit(repo, username, email)

    # #delete all other branches
    # for b in repo.branches.local:
    #     if(b != 'new'):
    #         repo.branches.delete(b)

    # #rename new branch to main
    # repo.branches['new'].rename('main')

    # #delete all remotes
    # n = len(repo.remotes)-1
    # for r in range(0, len(repo.remotes)):
    #     repo.remotes.delete(repo.remotes[n].name)
    #     n -= 1

    # #create a new remote origin
    # repo.remotes.create('origin', github_url)

    # index = repo.index
    # index.read()