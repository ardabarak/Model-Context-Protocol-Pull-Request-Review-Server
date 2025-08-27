import os
import requests
import traceback
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') #using specified token

def fetch_pr_changes(repo_owner: str, repo_name: str, pr_number: int) -> list:

    print(f" Fetching Pull Request changes for {repo_owner}/{repo_name}#{pr_number}")
    
    # Fetch Pull Reqs
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    files_url = f"{pr_url}/files"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
    try:
        # Get Pull Req data
        pr_response = requests.get(pr_url, headers=headers)
        pr_response.raise_for_status()
        pr_data = pr_response.json()
        
        # Get file changes
        files_response = requests.get(files_url, headers=headers)
        files_response.raise_for_status()
        files_data = files_response.json()
        
        # Concat Pull Req data with file changes
        changes = []
        for file in files_data:
            change = {
                'filename': file['filename'],
                'status': file['status'],  # added, modified, removed
                'additions': file['additions'],
                'deletions': file['deletions'],
                'changes': file['changes'],
                'patch': file.get('patch', ''),  
                'raw_url': file.get('raw_url', ''),
                'contents_url': file.get('contents_url', '')
            }
            changes.append(change)
        
        # Add Pull Req data
        pr_info = {
            'title': pr_data['title'],
            'description': pr_data['body'],
            'author': pr_data['user']['login'],
            'created_at': pr_data['created_at'],
            'updated_at': pr_data['updated_at'],
            'state': pr_data['state'],
            'total_changes': len(changes),
            'changes': changes
        }
        
        print(f"Fetched {len(changes)} changes successfully")
        return pr_info
        
    except Exception as e:
        print(f"Error in fetching Pull Request changes: {str(e)}")
        traceback.print_exc()
        return None
