# From here all FIXTURES can be shared by any test
# Do not import this file into tests - it gets read by pytest by default

import pytest, time, datetime, os, logging

# Will output this stuff in the header when pytest is run
def pytest_report_header(config):
    outputList = []
    outputList.append("\tAutomated Testing Framework")
    outputList.append("Author: 0xLucyfer")
    if config.getoption("verbose") > 0:
        outputList.append("Verbose: Enabled")
    return outputList

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # print('\nrep:', rep)

    # we only look at actual failing test calls, not setup
    if (rep.when == "call" or rep.when == "teardown") and rep.failed:
        mode = "a" if os.path.exists("tests/reports/failures.txt") else "w"
        
        # print('\nrep.when:', rep.when)
        # print('rep.FAILED:', rep.failed)
        # print('mode:', mode)
        # print()
        
        with open("backend/tests/reports/failures.txt", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""

            f.write(rep.when + " - " + rep.nodeid + extra + "\n")

@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    outcome = yield

    rep = outcome.get_result()
    now = time.time()

    totalPassed = 0
    totalFailed = 0
    totalDuration = 0.00

    for passed in terminalreporter.stats.get('passed', []):  # type: TestReport
        totalPassed = totalPassed + 1
        totalDuration = totalDuration + passed.duration
        # print('passed! node_id:%s, duration: %s, details: %s' % (passed.nodeid,
        #                                                         passed.duration,
        #                                                         str(passed.longrepr)))
    
    for failed in terminalreporter.stats.get('failed', []):  # type: TestReport
        totalFailed = totalFailed + 1
        totalDuration = totalDuration + failed.duration
        # print('failed! node_id:%s, duration: %s, details: %s' % (failed.nodeid,
        #                                                          failed.duration,
        #                                                          str(failed.longrepr)))
    totalTests = totalFailed + totalPassed
    print('\n---')
    print('- Total Tests         :', totalTests)
    print('- Total Passed        :', totalPassed)
    print('- Total Failed        :', totalFailed)
    print('- Total Test Duration : {:0.3} seconds'.format(totalDuration))
    print('- Finished            : {}'.format(time.strftime('%d %b %X', time.localtime(now))))
    print('-----------------')