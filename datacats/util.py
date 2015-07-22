"""
module datacats.util contains small helper elements reused accross the package
"""


def function_as_step(func, description=None):
    """
    Returns a tuple of function and first string of docstring
    to provide the user is some details on what the function does

    For procedures with a lot of steps or that take a long time
    one would like to print out a status message
    to the user to provide her with more details of
    what is going on.
    """
    if description:
        return func, description
    if func.__doc__:
        doc_lines = func.__doc__.split('\n')
        if len(doc_lines) > 0:
            return func, doc_lines[1].lstrip().rstrip()
    return func, func.__name__


def run_a_sequence_of_function_steps(list_of_functions, progress_tracker=None):
    """
    Some procedures include several steps being run
    we want to run them in a sequence and report progress
    to the caller (which is done in generic way with ProgressTracker)

    This accepts the list of functions and calls function_as_step on each
    to try generating one-line description from docstring so that
    the progress tracker can be updated with the status string.

    Sometimes it maybe needed to define custom progress messages,
    for example, when a step is defined with lambda function to also
    specify function's arguments.

    The suggested pattern then is to call function_as_step explicitely:
            list_of_functions = [
                 function_as_step(lambda: add(3,4),"Add two numbers")
            ]
    This function will recognize when the function_as_step has been called
    on an item in the list.
    """
    for step_num, step in enumerate(list_of_functions):
        if callable(step):
            # also support list item being a tuple of a func and a status string
            step = function_as_step(step)
        func, descr = step
        if progress_tracker:
            progress_tracker.update_state(
                state='PROGRESS',
                meta={
                    'current': step_num,
                    'total': len(list_of_functions),
                    'status': descr
                })
        func()
