import os

from datetime import date, timedelta

import logs as log
from git_interface import GitIntrerface
from logs import get_failed_tests_files


def cross_ref(job, build, repos_root_dir, since=None):
    git_interface = GitIntrerface(repos_root_dir)
    yesterday = date.today() - timedelta(1)
    since = since or yesterday.strftime("%Y-%m-%d")

    failed_tests = get_failed_tests_files(job, build)
    check_list = {}

    for test_name, values in failed_tests.iteritems():
        appearances = []
        for trace in values:
            method = trace[log.METHOD_KEY]
            file_path = trace[log.FILE_KEY]
            appearance = git_interface.get_log(file_path[0], method, since)
            if appearance:
                commit_info = [c.strip() for c in appearance.split('\n')
                               if c.strip()]
                appearances.append({log.METHOD_KEY: method,
                                    log.FILE_KEY: os.path.join(*file_path),
                                    'commit_info': commit_info})
        check_list[test_name] = appearances

    return check_list
