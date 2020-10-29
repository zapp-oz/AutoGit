import git_ops
import os
import shutil
import pygit2

def main():
    cwd = os.getcwd()
    repo_path = os.path.join(cwd, '../repo')
    repo = git_ops.clone('https://github.com/zapp-oz/test', repo_path)

    repo = git_ops.delete_history(
        repo_path,
        repo, 
        'shresth', 
        'shresthdewan@gmail.com', 
        'https://github.com/zapp-oz/test_project.git'
    )

    shutil.rmtree(repo_path)

if __name__ == "__main__":
    main()