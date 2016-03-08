import os
import re

import commands
from work import work

JE_ROOT_DIR = os.path.expanduser('~/.je')
JE_WORK_DIR = 'work'
JE_FAILED_DIR = 'failed'

METHOD_KEY = 'method'
FILE_KEY = 'file'


def get_failed_tests_files(job, build):

    tests_log_dir_path = work.failed_dir(job, build)

    logs = {}

    if not os.path.isdir(tests_log_dir_path):
        commands.report(job, build, failed=True)

    for log_name in os.listdir(tests_log_dir_path):
        log_path = os.path.join(tests_log_dir_path, log_name)
        with open(log_path, 'rb') as l:
            logs[log_name[:log_name.rindex('.')]] = \
                _extract_cloudify_files_and_functions_from_trace(l.read())

    return logs


def _extract_cloudify_files_and_functions_from_trace(log):
    # TODO: move from working with the str log to json log (cache)
    start_index = log.index('error stacktrace:')
    end_index = log.index('stdout')
    stack_trace = \
        log[start_index: end_index].split('\n')[1:]
    # time.sleep(5)
    # stack_trace = jenkins.fetch_build(job, build)['stack_trace']

    tracing = []

    for line in stack_trace:
        if line.strip().startswith('File'):
            affecting_file = \
                re.search('\".*\"', line).group(0).replace('"', '')
            affecting_method = line[line.rindex(','):].strip().split()[2]
            if affecting_file.startswith('/env/cloudify-'):
                tracing.append({FILE_KEY: affecting_file.replace('/env/', '')
                               .split('/'),
                                METHOD_KEY: affecting_method})

    return tracing
