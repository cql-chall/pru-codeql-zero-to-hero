import re
import os
import subprocess

from flask import Flask, request
app = Flask(__name__)


@app.route("/command1")
def command_injection1():
    files = request.args.get('files', '')
    # Use an allowlist of acceptable file names
    allowed_files = ["file1", "file2", "file3"]
    if files in allowed_files:
        subprocess.run(["ls", files])
    else:
        return "Invalid file name", 400


@app.route("/command2")
def command_injection2():
    files = request.args.get('files', '')
    # Use an allowlist of acceptable file names
    allowed_files = ["file1", "file2", "file3"]
    if files in allowed_files:
        subprocess.run(["ls", files])
    else:
        return "Invalid file name", 400


@app.route("/path-exists-not-sanitizer")
def path_exists_not_sanitizer():
    """os.path.exists is not a sanitizer

    This small example is inspired by real world code. Initially, it seems like a good
    sanitizer. However, if you are able to create files, you can make the
    `os.path.exists` check succeed, and still be able to run commands. An example is
    using the filename `not-there || echo pwned`.
    """
    path = request.args.get('path', '')
    # Use an allowlist of acceptable paths
    allowed_paths = ["/path1", "/path2", "/path3"]
    if path in allowed_paths and os.path.exists(path):
        subprocess.run(["ls", path])
    else:
        return "Invalid path", 400
