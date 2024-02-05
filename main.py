import subprocess
import requests
BLACK = '\033[90m'
FAIL = '\033[91m'
GREEN = '\033[92m'
WARNING = '\033[93m'
BLUE = '\033[94m'
PINK = '\033[95m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
ITALICIZED = '\033[3m'
UNDERLINE = '\033[4m'

def is_git_installed():
    try:
        # Run 'git --version' command and capture the output
        result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the return code is 0, indicating success
        if result.returncode == 0:
            print("Git is installed. Version:", result.stdout.strip())
            return True
        else:
            print("Git is not installed.")
            return False
    except FileNotFoundError:
        print("Git is not installed.")
        return False


def get_latest_commit_sha(owner, repo, branch='main'):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/commits/{branch}'
    response = requests.get(api_url)

    if response.status_code == 200:
        commit_data = response.json()
        return commit_data['sha']
    else:
        raise Exception(f"Failed to fetch commit information. Status code: {response.status_code}")


def get_local_commit_sha():
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Failed to get local commit SHA. Error: {result.stderr}")
    except FileNotFoundError:
        raise Exception("Git is not installed.")


def git_pull():
    try:
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        print("Git pull successful.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git pull failed. Error: {e.stderr}")


if is_git_installed():
    repo_owner = 'hexs'
    repo_name = 'test'

    try:
        local_commit = get_local_commit_sha()
        latest_commit = get_latest_commit_sha(repo_owner, repo_name)

        if local_commit != latest_commit:
            print("Local and remote commits are not the same. Performing git pull.")
            git_pull()
        else:
            print("Local and remote commits are already in sync.")
    except Exception as e:
        print(f"Error: {str(e)}")
