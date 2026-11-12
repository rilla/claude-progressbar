import json
import os
import stat


def private_dir(path):
    os.makedirs(path, mode=0o700, exist_ok=True)
    if hasattr(os, "getuid"):
        st = os.lstat(path)
        if not stat.S_ISDIR(st.st_mode):
            raise PermissionError(f"{path} is not a directory")
        if st.st_uid != os.getuid():
            raise PermissionError(f"{path} belongs to someone else")
        if st.st_mode & 0o077:
            os.chmod(path, 0o700)
    return path


def state_dir(env, fallback):
    return private_dir(os.path.join(os.environ.get(env) or fallback, "claude-progressbar"))


def write_atomic(path, payload):
    tmp = f"{path}.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(payload)
    try:
        os.replace(tmp, path)
    except PermissionError:
        os.remove(tmp)


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}
