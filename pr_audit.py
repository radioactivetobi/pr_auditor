import requests
import argparse

def get_merged_prs_without_approved_reviews(repo_name, token):
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
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        pulls = response.json()

        # Iterate through each pull request
        for pr in pulls:
            # Check if the pull request was merged
            if pr['merged_at']:
                # Construct the URL for the reviews of the pull request
                reviews_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr['number']}/reviews"
                # Get the reviews of the pull request
                reviews_response = requests.get(reviews_url, headers=headers)
                reviews_response.raise_for_status()
                reviews = reviews_response.json()

                # Check if there are any approved reviews
                approved_reviews = [r for r in reviews if r['state'] == 'APPROVED']

                # If there are no approved reviews, add the pull request to the list
                if not approved_reviews:
                    merged_prs_without_approved_reviews.append(pr)

        return merged_prs_without_approved_reviews

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

def get_repositories(organization, token):
    url = f'https://api.github.com/orgs/{organization}/repos'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json()
        return [repo['full_name'] for repo in repos]
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

def main():
    parser = argparse.ArgumentParser(description='Audit merged PRs without approved reviews.')
    parser.add_argument('-r', '--repo_name', type=str, help='The name of the repository (format: owner/repo)')
    parser.add_argument('-o', '--organization', type=str, help='The name of the organization')
    parser.add_argument('-p', '--token', required=True, type=str, help='Your personal access token')
    
    args = parser.parse_args()
    
    token = args.token
    
    if args.repo_name:
        repo_name = args.repo_name
        merged_prs_without_approved_reviews = get_merged_prs_without_approved_reviews(repo_name, token)
        
        if merged_prs_without_approved_reviews is not None and merged_prs_without_approved_reviews:
            print(f'\nRepository: {repo_name}')
            print('Merged Pull Requests without approved reviews:')
            for pr in merged_prs_without_approved_reviews:
                print(f"#{pr['number']} - {pr['title']}")
    elif args.organization:
        organization = args.organization
        repositories = get_repositories(organization, token)
        
        if repositories is not None:
            for repo_name in repositories:
                merged_prs_without_approved_reviews = get_merged_prs_without_approved_reviews(repo_name, token)
                
                if merged_prs_without_approved_reviews is not None and merged_prs_without_approved_reviews:
                    print(f'\nRepository: {repo_name}')
                    print('Merged Pull Requests without approved reviews:')
                    for pr in merged_prs_without_approved_reviews:
                        print(f"#{pr['number']} - {pr['title']}")
    else:
        print('Either repository name or organization name must be provided.')

if __name__ == '__main__':
    main()
