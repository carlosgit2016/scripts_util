# All files with the absolute path
ls -1 | xargs -I {} echo "$(pwd)/{}"