import requests
import argparse
from datetime import datetime
from termcolor import colored
import csv

def fetch_all_repos_from_org(org_name, token):
    repos = []
    page = 1
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    while True:
        url = f'https://api.github.com/orgs/{org_name}/repos?page={page}&per_page=100'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(colored(f'Error fetching repositories from organization: {response.text}', 'red'))
            return []
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_commits_without_successful_status_checks(repo_name, token, start_date):
    base_url = f'https://api.github.com/repos/{repo_name}/commits'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'per_page': 100,
    }

    commits_without_successful_status_checks = []
    page = 1

    while True:
        params['page'] = page
        url = f"{base_url}?per_page=100&page={page}"

        try:
            print(colored(f'Fetching commits for repository {repo_name}, page {page}...', 'yellow'))
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            commits = response.json()

            if not commits:
                break

            for commit in commits:
                commit_date = datetime.fromisoformat(commit['commit']['committer']['date'][:-1])
                if commit_date >= start_date:
                    statuses_url = f"https://api.github.com/repos/{repo_name}/commits/{commit['sha']}/status"
                    print(colored(f'Fetching status checks for commit {commit["sha"]}', 'yellow'))
                    statuses_response = requests.get(statuses_url, headers=headers)
                    statuses_response.raise_for_status()
                    status_data = statuses_response.json()

                    if status_data['state'] != 'success':
                        commit['repo_name'] = repo_name
                        commits_without_successful_status_checks.append(commit)

            page += 1

        except requests.exceptions.RequestException as e:
            print(colored(f'Error: {e}', 'red'))
            return None

    return commits_without_successful_status_checks

def main():
    parser = argparse.ArgumentParser(description='GitHub Commit Auditor for Status Checks')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--repo', help='GitHub repository in the format "owner/repo"')
    group.add_argument('-o', '--org', help='GitHub organization name')
    parser.add_argument('-p', '--token', help='GitHub token for API authentication', required=True)
    parser.add_argument('-s', '--start_date', help='Start date for commit filtering in the format "YYYY-MM-DD"', required=True)
    parser.add_argument('-f', '--file', help='Output CSV file name', required=True)

    args = parser.parse_args()
    start_date = datetime.fromisoformat(args.start_date)

    repos_to_check = []

    if args.repo:
        repos_to_check.append(args.repo)
    elif args.org:
        print(colored(f'Fetching repositories from organization: {args.org}', 'yellow'))
        repos = fetch_all_repos_from_org(args.org, args.token)
        repos_to_check.extend([repo['full_name'] for repo in repos])

    commits = []
    for repo in repos_to_check:
        commits.extend(get_commits_without_successful_status_checks(repo, args.token, start_date))

    if not commits:
        print(colored('No commits found with unsuccessful status checks.', 'green'))
        return

    with open(args.file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Repo', 'Commit SHA', 'Message', 'Date', 'Author', 'Link'])
        for commit in commits:
            writer.writerow([commit['repo_name'], commit['sha'], commit['commit']['message'], commit['commit']['committer']['date'], commit['commit']['author']['name'], commit['html_url']])

    print(colored(f"Results saved to {args.file}", 'green'))

if __name__ == '__main__':
    main()
