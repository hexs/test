import subprocess
import requests

BLACK = '\033[90m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PINK = '\033[95m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
ITALICIZED = '\033[3m'
UNDERLINE = '\033[4m'


def is_git_installed():
    try:
        result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(f"{GREEN}{ITALICIZED}Git is installed. Version:{ENDC}", result.stdout.strip())
            return True
        else:
            print(f"{RED}{ITALICIZED}Git is not installed.{ENDC}")
            return False
    except FileNotFoundError:
        print(f"{RED}{ITALICIZED}Git is not installed.{ENDC}")
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
        print(f"{GREEN}{ITALICIZED}Git pull successful.{ENDC}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git pull failed. Error: {e.stderr}")


if is_git_installed():
    repo_owner = 'hexs'
    repo_name = 'test'

    try:
        local_commit = get_local_commit_sha()
        latest_commit = get_latest_commit_sha(repo_owner, repo_name)

        if local_commit != latest_commit:
            print(f"Local and remote commits are {RED}{ITALICIZED}not the same. Performing git pull.{ENDC}")
            git_pull()
        else:
            print(f"Local and remote commits are {GREEN}{ITALICIZED}already in sync.{ENDC}")
    except Exception as e:
        print(f"{RED}{ITALICIZED}Error:{ENDC} {RED}{str(e)}{ENDC}")
