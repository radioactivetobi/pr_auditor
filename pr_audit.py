import requests
import argparse
import csv
from datetime import datetime
from termcolor import colored

def get_merged_prs_without_approved_reviews(repo_name, token, start_date):
    url = f'https://api.github.com/repos/{repo_name}/pulls'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'state': 'closed',
    }

    # List to store merged PRs without approved reviews
    merged_prs_without_approved_reviews = []
    
    try:
        # Get the list of closed pull requests
        print(colored(f'Fetching closed pull requests for repository {repo_name}...', 'yellow'))
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        pulls = response.json()

        # Iterate through each pull request
        for pr in pulls:
            # Check if the pull request was merged
            if pr['merged_at'] and datetime.fromisoformat(pr['merged_at'][:-1]) >= start_date:
                # Construct the URL for the reviews of the pull request
                reviews_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr['number']}/reviews"
                # Get the reviews of the pull request
                print(colored(f'Fetching reviews for pull request #{pr["number"]}', 'yellow'))
                reviews_response = requests.get(reviews_url, headers=headers)
                reviews_response.raise_for_status()
                reviews = reviews_response.json()

                # Check if there are any approved reviews
                approved_reviews = [r for r in reviews if r['state'] == 'APPROVED']

                # If there are no approved reviews, add the pull request to the list
                if not approved_reviews:
                    pr['reviews'] = reviews
                    merged_prs_without_approved_reviews.append(pr)

        return merged_prs_without_approved_reviews

    except requests.exceptions.RequestException as e:
        print(colored(f'Error: {e}', 'red'))
        return None

def get_repositories(organization, token):
    url = f'https://api.github.com/orgs/{organization}/repos'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    try:
        print(colored(f'Fetching repositories for organization {organization}...', 'yellow'))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json()
        return [repo['full_name'] for repo in repos]
    except requests.exceptions.RequestException as e:
        print(colored(f'Error: {e}', 'red'))
        return None

def main():
    parser = argparse.ArgumentParser(description='Audit merged PRs without approved reviews.')
    parser.add_argument('-r', '--repo_name', type=str, help='The name of the repository (format: owner/repo)')
    parser.add_argument('-o', '--organization', type=str, help='The name of the organization')
    parser.add_argument('-p', '--token', required=True, type=str, help='Your personal access token')
    parser.add_argument('-s', '--start_date', required=True, type=str, help='The start date (format: YYYY-MM-DD)')
    parser.add_argument('-f', '--file', type=str, help='The name of the CSV file to save the output', default='output.csv')
    
    args = parser.parse_args()
    
    token = args.token
    start_date = datetime.fromisoformat(args.start_date)
    file = args.file
    
    if args.repo_name:
        repo_name = args.repo_name
        print(colored('Auditing merged pull requests without approved reviews...', 'green'))
        merged_prs_without_approved_reviews = get_merged_prs_without_approved_reviews(repo_name, token, start_date)

        if merged_prs_without_approved_reviews is not None:
            if merged_prs_without_approved_reviews:
                # Save the output to a CSV file
                print(colored(f'Saving the output to CSV file {file}...', 'green'))
                with open(file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Repository', 'PR Number', 'Title', 'Sent Date', 'Merge Date', 'Link', 'From', 'Reviewers'])
                    for pr in merged_prs_without_approved_reviews:
                        reviewers = [r['user']['login'] for r in pr['reviews']]
                        writer.writerow([repo_name, pr['number'], pr['title'], pr['created_at'], pr['merged_at'], pr['html_url'], pr['user']['login'], ', '.join(reviewers) if reviewers else 'None'])
            else:
                print(colored('\nAll merged pull requests have approved reviews.', 'green'))
    elif args.organization:
        organization = args.organization
        repositories = get_repositories(organization, token)
        
        if repositories is not None:
            print(colored('Auditing merged pull requests without approved reviews for each repository...', 'green'))
            # Save the output to a CSV file
            print(colored(f'Saving the output to CSV file {file}...', 'green'))
            with open(file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Repository', 'PR Number', 'Title', 'Sent Date', 'Merge Date', 'Link', 'From', 'Reviewers'])
                for repo_name in repositories:
                    merged_prs_without_approved_reviews = get_merged_prs_without_approved_reviews(repo_name, token, start_date)
                    
                    if merged_prs_without_approved_reviews is not None and merged_prs_without_approved_reviews:
                        for pr in merged_prs_without_approved_reviews:
                            reviewers = [r['user']['login'] for r in pr['reviews']]
                            writer.writerow([repo_name, pr['number'], pr['title'], pr['created_at'], pr['merged_at'], pr['html_url'], pr['user']['login'], ', '.join(reviewers) if reviewers else 'None'])
        else:
            print(colored('No repositories found.', 'red'))
    else:
        print(colored('Either repository name or organization name must be provided.', 'red'))

if __name__ == '__main__':
    main()
