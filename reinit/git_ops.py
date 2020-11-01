import os
import pygit2
import json
import requests

class GithubOps:

    def __init__(self, username, password):
        
        self._username = username
        self._password = password

    def new_github_repo(self, repo_name):
        
        response = requests.post(
            url = 'https://api.github.com/user/repos', 
            headers = {
                'Accept': 'application/vnd.github.v3+json'
            }, 
            data = json.dumps({
                'name': repo_name
            }), 
            auth = (self._username, self._password)
        )
        
        if response.status_code == 201:
            return True
        else:
            return False

    def delete_github_repo(self, repo_name):

        response = requests.delete(
                url = 'https://api.github.com/repos/' + self._username + '/' + repo_name,
                headers = {
                'Accept': 'application/vnd.github.v3+json'
                },
                auth = (self._username, self._password)
            )

        if response.status_code == 204:
            return True
        else: 
            return False
    


class GitOps:

    def __init__(self, username, password, local_repo_path, local_repo_name):
        self._username = username
        self._password = password
        self._local_repo_path = local_repo_path
        self._local_repo_name = local_repo_name

    #clone git repo and initialize submodules
    def clone(self, github_repo_url):

        cloned_repo = pygit2.clone_repository(
            github_repo_url, 
            os.path.join(self._local_repo_path, self._local_repo_name),
            callbacks = pygit2.RemoteCallbacks(
                    pygit2.UserPass(
                        self._username, 
                        self._password
                    )
                )
        )

        cloned_repo.init_submodules()

        cloned_repo.update_submodules()


    def create_commit(self, ref, commit_message):

        #get the local git repo
        repo = pygit2.Repository(
            os.path.join(self._local_repo_path, self._local_repo_name)
        )

        #add all files to staging area
        index = repo.index
        index.add_all()
        index.write()

        #create a new tree empty tree object
        author = pygit2.Signature(
            self._username + ' Author', 
            self._username + '@authors.tld'
        )
        
        committer = pygit2.Signature(
            self._username + ' Committer', 
            self._username + '@committers.tld'
        )
        
        tree = index.write_tree()

        #create a new commit in a new branch
        repo.create_commit(
            ref,
            author,
            committer,
            commit_message,
            tree,
            []
        )

        #change the HEAD to new branch
        repo.checkout(ref)

    def set_new_remote(self, remote_name, remote_url):

        #get the local git repo
        repo = pygit2.Repository(
            os.path.join(self._local_repo_path, self._local_repo_name)
        )

        try:
            repo.remotes.create(
                remote_name, 
                remote_url
            )
            return True

        except Exception:
            return False

    def push_repo(self, ref, remote_name):

        #get the local git repo
        repo = pygit2.Repository(
            os.path.join(self._local_repo_path, self._local_repo_name)
        )

        try:
            repo.remotes[remote_name].push(
                [ref],
                pygit2.RemoteCallbacks(
                    pygit2.UserPass(
                        self._username, 
                        self._password
                    )
                )
            )
            return True

        except Exception:
            return False
    

    #delete all the git repo history
    def reset_git(self):

        local_repo_path = os.path.join(self._local_repo_path, self._local_repo_name)

        #get the local git repo
        repo = pygit2.Repository(
            local_repo_path
        )

        #delete README.md
        if os.path.exists(os.path.join(local_repo_path, 'README.md')):
            os.remove(os.path.join(local_repo_path, 'README.md'))

        #delete License.txt
        if(os.path.exists(os.path.join(local_repo_path, 'LICENSE'))):
            os.remove(os.path.join(local_repo_path, 'LICENSE'))

        self.create_commit('refs/heads/new', 'Init Commit')

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