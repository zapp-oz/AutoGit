import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reinit')))

import argparse
import git_ops
import shutil
from tkinter import filedialog

def getargs():
    #initialize the parser
    parser = argparse.ArgumentParser()

    #define optional arguments groups
    required_args = parser.add_argument_group('required arguments:')

    #add arguments to the groups
    required_args.add_argument('--username', help='github username\n', required=True)
    required_args.add_argument('--password', help='github password\n', required=True)
    required_args.add_argument('--input_repo', help='clone url\n', required=True)
    required_args.add_argument('--output_repo_name', help='new repo name\n', required=True)

    #return the parsed args
    return parser.parse_args()

def getdir():

    input_dir = filedialog.askdirectory(
        title='new repo location'
    )
    return input_dir

def main():
    args = getargs()
    local_repo_path = getdir()

    #setting up local repo for the repo to be cloned
    local_git_repo = git_ops.GitOps(
        args.username,
        args.password,
        local_repo_path,
        args.output_repo_name
    )

    status = local_git_repo.clone(args.input_repo)

    if not status:
        if os.path.isdir(os.path.join(local_repo_path, args.output_repo_name)):
            shutil.rmtree(os.path.join(local_repo_path, args.output_repo_name))
        sys.exit('Error cloning the repo')

    status = local_git_repo.reset_git()

    if not status:
        shutil.rmtree(os.path.join(local_repo_path, args.output_repo_name))
        sys.exit('Error re-initializing the repo')

    status = local_git_repo.set_new_remote(
        'origin',
        'https://github.com/' + args.username + '/' + args.output_repo_name
    )

    if not status:
        shutil.rmtree(os.path.join(local_repo_path, args.output_repo_name))


    #pushing reset repo to github
    remote_github_repo = git_ops.GithubOps(args.username, args.password)

    status = remote_github_repo.new_github_repo(args.output_repo_name)

    if not status:
        shutil.rmtree(os.path.join(local_repo_path, args.output_repo_name))
        sys.exit('Error creating github repo')

    status = local_git_repo.push_repo(
        'refs/heads/main',
        'origin'
    )

    if not status:
        remote_github_repo.delete_github_repo(args.output_repo_name)
        shutil.rmtree(os.path.join(local_repo_path, args.output_repo_name))
        sys.exit('Error pushing the code to gihub')

if __name__ == '__main__':
    main()