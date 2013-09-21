# coding=utf-8
import functools
import hashlib
import os

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()

def get_hash_info(root):
    result = {}
    for dir_path, dir_name, file_names in os.walk(root):
        abs_file_names = [os.path.join(dir_path, file_name) for file_name in file_names]
        for abs_file_name in abs_file_names:
            hash = hashfile(open(abs_file_name, 'rb'), hashlib.sha256())
            if hash in result:
                result[hash].append(abs_file_name)
            else:
                result[hash] = [abs_file_name]
    return result
    

def pick(file1, file2):
    len1, len2 = map(len, map(os.path.split, (file1, file2)))
    if len1 > len2:
        return file1
    elif len1 < len2:
        return file2
    else:
        return len(file1) < len(file2) and file1 or file2
    

def remove_redundant(file_names):
    final_pick = functools.reduce(pick, file_names)
    [os.remove(f) for f in file_names if f != final_pick]


def remove_if_empty_folder(walk_info):
    dir_path, dir_name, file_names = walk_info
    if dir_name or file_names:
        pass
    else:
        os.rmdir(dir_path)


if __name__ == '__main__':
    root = ""
    hash_info = get_hash_info(root)
    
    [remove_redundant(info) for info in hash_info.values()]
    [os.rmdir(path) for path, dir, files in os.walk(root) if (not dir) and (not files)]  
