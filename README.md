# Audit Merged Pull Requests Without Approved Reviews

This script audits merged pull requests in a given GitHub repository or all repositories of a given organization to identify any that were merged without approved reviews. It leverages the GitHub API to fetch the list of merged pull requests and their associated reviews.

## Requirements

- Python 3
- A GitHub personal access token

## Installation

1. Clone the repository and navigate to its directory.

    ```sh
    git clone https://github.com/radioactivetobi/pr_auditor.git
    cd pr_auditor
    ```

2. Install the required Python packages.

    ```sh
    pip install -r requirements.txt
    ```

## Usage

The script can be run from the command line with the following arguments:

- `-r`, `--repo_name`: The name of the repository in the format `owner/repo`.
- `-o`, `--organization`: The name of the organization.
- `-p`, `--token`: Your personal access token (required).
- `-s`, `--start_date`: The start date in the format `YYYY-MM-DD` (required).

Either `repo_name` or `organization` must be provided.

### Example

To audit a single repository:

```sh
python script.py -r owner/repo -p your-token -s 2022-01-01
```

To audit all repositories of an organization:

```sh
python script.py -o organization -p your-token -s 2022-01-01
```

## Output

The script will print the merged pull requests without approved reviews for each audited repository. For each pull request, it will print:

- The pull request number and title.
- The date the pull request was created.
- The date the pull request was merged.
- The link to the pull request on GitHub.
- The username of the user who created the pull request.
- The usernames of the reviewers who reviewed the pull request. If there are no reviewers, it will print 'None'.

## Note

The script uses the `requests` library to make HTTP requests to the GitHub API. It uses a personal access token for authentication. Make sure to generate a personal access token with the appropriate scopes (`repo` and `read:org`) and pass it as an argument when running the script.

## License

[MIT](LICENSE)

---
