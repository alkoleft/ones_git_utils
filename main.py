import os
from git import Repo
import diff_utils
from colorama import Fore, Back, Style

path = r'F:\dev\python\ones_doc_gen'
repo = Repo(path)

for item in diff_utils.get_files(repo):
    print(item)

hcommit = repo.head.commit

files_to_index = []

for item in hcommit.diff(None, create_patch=True):
    print('>>')
    files_to_index.append(item.b_path)
    print(Back.LIGHTBLACK_EX + os.path.join(path, item.a_path))
    print(Back.RESET)

    diff_str = item.diff.decode("utf-8")

    line_index = 0
    for line in diff_str.splitlines():
        if line[0] == ' ':
            line_index += 1
            continue
        if line[:2] == '@@':
            print('-------------------')
            print(line[3: line.index('@@', 3) - 1])
            line_index = int(line[4: line.index(',', 4)]) - 1
        else:
            print(''.join([
                str(line_index).zfill(4),
                ': ',
                Fore.RED if line[0] == '-' else Fore.GREEN,
                'DEL: ' if line[0] == '-' else 'ADD: ',
                line[1:],
                Fore.RESET]))
        if line[0] != '-':
            line_index += 1

repo.index.add(files_to_index)