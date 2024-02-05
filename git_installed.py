import subprocess


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


# Check if Git is installed
is_git_installed()
