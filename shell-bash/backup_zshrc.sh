#!/bin/bash

set -e

temp=$(mktemp -d)
cd $temp

git clone "git@github.com:carlosgit2016/backups.git"

cd backups

git config user.name "carlosgit2016" && git config user.email carlosggflor@gmail.com

cp -f ~/.zshrc .

# Get a list of added and modified files
files_to_check=$(git status --porcelain | grep -e '[AM]' | cut -c 4-)

for file in $files_to_check; do
    # Check if the file has deletions
    if git diff -- "$file" | grep '^-' > /dev/null; then
        # If the file has deletions, unstage it
        git reset HEAD "$file"
    fi
done

# Checking if there is anything to commit
if [[ -n $(git status --porcelain) ]]; then
    msg="backup-$(date +%e/%m/%G\ %H:%M)"
    git commit -m "$msg"
    git branch -M main
    git push -u origin main
fi
