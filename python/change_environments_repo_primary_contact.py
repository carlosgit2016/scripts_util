from pathlib import Path
import pathlib

def run():
    path = pathlib.Path('/home/cflor/git/eFleetSuite/eld-environments-lowers/environments')
    for p in path.iterdir():
        childpath = Path(f'{p}/terragrunt/us-east-1/env.hcl')
        if (childpath.is_file()):
            file_content = open(childpath, 'r').read()
            # Replace primary contact
            file_content = file_content.replace("<old_name>", "<new_name>")
            # Replace email contact
            file_content = file_content.replace("<old_email>", "<new_email>")
            open(childpath, 'w+').write(file_content)


if __name__ == "__main__":
    run()
