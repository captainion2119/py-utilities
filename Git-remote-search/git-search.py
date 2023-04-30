"""
This code goes through every existing file on the mentioned drive and checks for git repositories, and when it finds a repository,
it runs git remote -v and prints the output onto a output.txt file.

NOTE: change {ENTER_DRIVE_NAME_HERE} to your drive name.
"""


import os
import subprocess
# Directory to start searching from
root_dir = '{ENTER_DRIVE_NAME_HERE}:\\'
# Search for .git folders
git_dirs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if '.git' in dirnames:
        git_dirs.append(os.path.join(dirpath, '.git'))
    print(f"Searching {dirpath}...")
# Execute command for each git directory
for git_dir in git_dirs:
    try:
        # Get parent directory of .git folder
        parent_dir = os.path.abspath(os.path.join(git_dir, os.pardir))
      
        # Add parent directory to safe directories
        subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', parent_dir], check=True)
      
        # Run git remote command and save output to file
        output = subprocess.check_output(['git', '-C', parent_dir, 'remote', '-v'])
        with open('output.txt', 'a') as f:
            f.write(f"\n\n{parent_dir}:\n{output.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Error while executing command for {parent_dir}: {e}")
    except Exception as e:
        print(f"Error while processing {parent_dir}: {e}")
