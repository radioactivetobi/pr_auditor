# Audit Merged PRs Without Approved Reviews

This script checks for merged pull requests without approved reviews in a GitHub repository or across all repositories of a GitHub organization.

## Requirements

- Python 3.6 or higher
- `requests` package
- `termcolor` package

## Installation

1. Clone the repository:

```
git clone https://github.com/radioactivetobi/pr_auditor.git
cd pr_auditor
```

2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

You can run the script using the following command:

```
python script.py -p YOUR_TOKEN -s START_DATE [-r REPO_NAME | -o ORGANIZATION] [-f FILE]
```

- `YOUR_TOKEN`: Your personal access token. Required.
- `START_DATE`: The start date in the format `YYYY-MM-DD`. Required.
- `REPO_NAME`: The name of the repository in the format `owner/repo`. Optional. Either `REPO_NAME` or `ORGANIZATION` must be provided.
- `ORGANIZATION`: The name of the organization. Optional. Either `REPO_NAME` or `ORGANIZATION` must be provided.
- `FILE`: The name of the CSV file to save the output. Optional. Default is `output.csv`.

For example:

```
python script.py -r owner/repo -p your-token -s 2022-01-01
```

or

```
python script.py -o organization -p your-token -s 2022-01-01 -f output.csv
```

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

## License

[MIT](LICENSE)
