# Technical Documentation

## Overview

The `pr_audit.py` script is designed to audit merged pull requests in a GitHub repository or across all repositories of a GitHub organization. Specifically, it checks for merged pull requests that do not have any approved reviews. The script fetches closed pull requests, checks if they were merged without any approved reviews, and then outputs the results into a CSV file.

## System Requirements

- Python 3.6 or higher.
- `requests` package.
- `termcolor` package.

## Installation

1. Clone the repository using the command:

```
git clone https://github.com/radioactivetobi/pr_auditor.git
cd pr_auditor
```

2. Install the required packages using the command:

```
pip install -r requirements.txt
```

## Execution

Run the script using the following command:

```
python pr_audit.py -p YOUR_TOKEN -s START_DATE [-r REPO_NAME | -o ORGANIZATION] [-f FILE]
```

Arguments:

- `YOUR_TOKEN`: Your personal access token. This is a required argument.
- `START_DATE`: The start date in the `YYYY-MM-DD` format from which the script will start checking the pull requests. This is a required argument.
- `REPO_NAME`: The name of the repository in the `owner/repo` format. This is an optional argument. Either `REPO_NAME` or `ORGANIZATION` must be provided.
- `ORGANIZATION`: The name of the organization. This is an optional argument. Either `REPO_NAME` or `ORGANIZATION` must be provided.
- `FILE`: The name of the CSV file to save the output. This is an optional argument. The default value is `output.csv`.

Example Usage:

```
python pr_audit.py -r owner/repo -p your-token -s 2022-01-01
```

or

```
python pr_audit.py -o organization -p your-token -s 2022-01-01 -f output.csv
```

## Functionality

The script consists of three main functions:

1. `get_merged_prs_without_approved_reviews`: This function fetches the closed pull requests from the specified repository, checks if they were merged, and if so, checks if they have any approved reviews. If a merged pull request does not have any approved reviews, it is added to a list which is then returned.

2. `get_repositories`: This function fetches all the repositories of the specified organization.

3. `main`: This is the main function that parses the command-line arguments, calls the other functions, and writes the results to a CSV file.

## Output

The script will save the merged pull requests without approved reviews to a CSV file with the following columns:

- `Repository`: The name of the repository.
- `PR Number`: The number of the pull request.
- `Title`: The title of the pull request.
- `Sent Date`: The date when the pull request was created.
- `Merge Date`: The date when the pull request was merged.
- `Link`: The link to the pull request.
- `From`: The user who created the pull request.
- `Reviewers`: The users who reviewed the pull request.

## Error Handling

The script uses the `requests.exceptions.RequestException` to handle any exceptions that may occur during the HTTP requests.

## License

The script is licensed under the MIT license.
