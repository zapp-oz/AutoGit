import git_ops
import os
import argparse
import sys

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

def main():
    args = getargs()

    cwd = os.getcwd()
    repo_path = os.path.join(cwd, '../' + args.output_repo_name)#fix this
    repo = git_ops.clone(args.input_repo, repo_path)

    git_ops.delete_history(
        repo_path,
        repo, 
        args.username, 
        args.username, #change this
        args.output_repo_name
    )

    status = git_ops.new_github_repo(
        args.username, 
        args.password, 
        args.output_repo_name
    )

    if not status:
        sys.exit('Error creating github repo')

    status = git_ops.push_repo(
        repo, 
        args.username, 
        args.password,
        args.output_repo_name
    )

    if not status:
        sys.exit('Error pushing the code to gihub')

if __name__ == "__main__":
    main()