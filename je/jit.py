import os

from datetime import date, timedelta

import logs as log
from git_interface import GitIntrerface
from logs import get_failed_tests_report


YESTERDAY = date.today() - timedelta(days=1)


def cross_ref(job, build, repos_root_dir, since=YESTERDAY):
    git_interface = GitIntrerface(repos_root_dir)
    if isinstance(since, basestring):
        day, month, year = (int(x) for x in since.split('.'))
        since = date(year if year > 2000 else year + 2000, month, day)

    managed_repos_names = os.listdir(git_interface.repos_root_dir)
    failed_tests = get_failed_tests_report(job, build, managed_repos_names)

    cross_list = {}

    for suite_name, tests in failed_tests.iteritems():
        cross_list[suite_name] = {}
        for test_name, methods in tests.iteritems():
            for method in methods:
                method_name = method[log.METHOD_KEY]
                file_path = method[log.FILE_KEY]
                appearance = git_interface.get_log(file_path[0],
                                                   method_name,
                                                   since)
                if appearance:
                    commit_info = [c.strip() for c in appearance.split('\n')
                                   if c.strip()]
                    cross_list[suite_name][test_name] = {
                        log.METHOD_KEY: method_name,
                        log.FILE_KEY: os.path.join(*file_path),
                        log.COMMIT_KEY: commit_info}

    return cross_list
