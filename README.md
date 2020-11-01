# Reinit

Reinit is a python library that allows you to re-initialize a git repository.
One can provide their username, password, new-output-repo name and input-repo url to the cli utility as arguments and the script will clean up the input repo, re-initialize it, and finally push it github.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install reinit.

```bash
pip install reinit
```

## Usage

```bash
reinit --username=[github_username] --password=[github_password] --input_repo=[any_github_repo_url] --output_repo_name=[new_name_for_cloned_repo]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)