import hashlib
import shutil
import os
import json


#Repository Initilization
def init_repo():
    if not os.path.exists('.mygit'):
        os.makedirs('.mygit/objects')
        os.makedirs('.mygit/refs/heads')
        with open('.mygit/HEAD', 'w') as f:
            f.write('refs/heads/main')
        with open('.mygit/refs/heads/main', 'w') as f:
            f.write('')
        print("Initialized empty repository in .mygit/")
    else:
        print("Repository already exists.")


#Staging files
def add_to_stage(file_path):
    ignore_list = load_ignore_file()
    if any(file_path.endswith(pattern) for pattern in ignore_list):
        print(f"Skipped adding {file_path} (ignored)")
        return

    staging_area = '.mygit/staging'
    os.makedirs(staging_area, exist_ok=True)
    dest = os.path.join(staging_area, file_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(file_path, dest)
    print(f"Added {file_path} to staging area.")


def load_ignore_file():
    if os.path.exists('.mygitignore'):
        with open('.mygitignore', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []


#Committing files
def commit(message):
    staging_area = '.mygit/staging'
    if not os.listdir(staging_area):
        print("Nothing to commit.")
        return

    commit_hash = hashlib.sha1(message.encode()).hexdigest()
    commit_dir = f".mygit/objects/{commit_hash}"
    os.makedirs(commit_dir)

    # Copy staged files
    for root, dirs, files in os.walk(staging_area):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), staging_area)
            dest = os.path.join(commit_dir, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(os.path.join(root, file), dest)

    # Write commit metadata
    head_ref = open('.mygit/HEAD').read().strip()
    parent = open(head_ref).read().strip(
    ) if os.path.exists(head_ref) else None
    metadata = {'message': message, 'parent': parent}
    with open(f'{commit_dir}/metadata.json', 'w') as f:
        json.dump(metadata, f)

    # Update HEAD
    with open(head_ref, 'w') as f:
        f.write(commit_hash)

    # Clear staging
    shutil.rmtree(staging_area)
    os.makedirs(staging_area)
    print(f"Committed: {message}")


#Viewing history
def log():
    head_ref = open('.mygit/HEAD').read().strip()
    commit_hash = open(head_ref).read().strip()

    while commit_hash:
        commit_dir = f".mygit/objects/{commit_hash}"
        with open(f'{commit_dir}/metadata.json') as f:
            metadata = json.load(f)
        print(f"Commit: {commit_hash}\nMessage: {metadata['message']}\n")
        commit_hash = metadata['parent']
