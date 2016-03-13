import re

from je.jenkins import jenkins

METHOD_KEY = 'method'
FILE_KEY = 'file'
COMMIT_KEY = 'commit_key'


def get_failed_tests_report(job, build, available_repos):

    log = jenkins.fetch_build(job, build)
    suites = log['test_report']['suites']
    failed_tests = {}
    for suite in suites:
        failed_tests[suite['name']] = {}
        for case in suite['cases']:
            if case['status'] == 'FAILED':
                failed_tests[suite['name']][case['name']] = {
                     'error_stack_trace': case['errorStackTrace'],
                     'error_details': case['errorDetails']
                }
        if len(failed_tests[suite['name']]) is 0:
            del(failed_tests[suite['name']])

    failed_tests_report = {}

    for suite, cases in failed_tests.iteritems():
        failed_tests_report[suite] = {}
        for case, props in cases.iteritems():
            tracing = []
            for line in props['error_stack_trace'].split('\n'):
                if line.strip().startswith('File'):
                    affecting_file_path = \
                        re.search('\".*\"', line).group(0).replace('"', '')
                    affecting_method = \
                        line[line.rindex(','):].strip().split()[2]
                    affected_file = \
                        affecting_file_path.replace('/env/', '').split('/')
                    if affected_file[0] in available_repos:
                        tracing.append({
                            FILE_KEY: affected_file,
                            METHOD_KEY: affecting_method
                        })

            failed_tests_report[suite][case] = tracing

    return failed_tests_report
