# -------------------------------------------------------------------------------
# -- Title       : Log Utilities
# -------------------------------------------------------------------------------
# -- Description: General logging functions
# -------------------------------------------------------------------------------


from datetime import datetime

CHAR_LENGTH = 60


def append_result_ok(test_results):
    """Add OK message to test result.

    Keyword arguments:
    test_results -- String with test results [str]
    """
    test_results += '..............OK \n'
    return test_results


def append_result_fail(test_results):
    """Add FAILED message to test result.

    Keyword arguments:
    test_results -- String with test results [str]
    """
    test_results += '..............FAILED \n'
    return test_results


def create_section(title, content):
    """Create a log Section.

    Keyword arguments:
    title -- Title for the section [str]
    content -- Content of the section [str]
    """
    title_str = '\n===================== ' + title + ' =====================\n'
    title_str += '=' * (len(title_str) - 2)

    content_str = '\n' + content + '\n'

    return title_str + content_str


def create_subsection(title, content):
    """Create a log SubSection.

    Keyword arguments:
    title -- Title for the subsection [str]
    content -- Content of the subsection [str]
    """
    title_str = '\n-----------------' + title + '-----------------\n'

    content_str = '\n' + content + '\n'

    return title_str + content_str


def create_subsubsection(title, content):
    """Create a log SubSubSection.

    Keyword arguments:
    title -- Title for the subsubsection [str]
    content -- Content of the subsubsection [str]
    """
    title_str = '\n- ' + title + '\n'

    content_str = '\n' + content

    return title_str + content_str


def create_test_section(title, description, content):
    """Create a log special Test Section.

    Keyword arguments:
    title -- Title for the Test section [str]
    description -- Short description of the tests [str]
    content -- Content of the Test Section [str]
    """
    title_str = '\n***************************************************************'
    title_str += '\n********************* ' + title + ' *********************\n'

    content_str = '\nDescription: ' + description + '\n'
    content_str += '\n' + content

    return title_str + content_str


def create_main_header(description=''):
    """Create a main header for the log.

    Keyword arguments:
    description -- Short description of the tests [str]
    """
    now = datetime.now()

    time_str = 'Test start date and time: {}/{}/{} at {}:{}:{} \n'.format(
        now.day, now.month, now.year, now.hour, now.minute, now.second)
    description_str = description + '\n'

    title = 'TEST LOG FILE'

    content = time_str + description_str

    header_str = create_section(title, content)

    return header_str
