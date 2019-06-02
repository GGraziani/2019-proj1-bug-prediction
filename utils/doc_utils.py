from utils.misc import indent

DOCSTRING = '''
2019-proj2-bug-prediction
by Gustavo Graziani

Commands:
{extract_feature_vectors}

TO SEE DETAILS ON EACH COMMAND, RUN
> python3 bug_prediction.py <command>
'''

MODULE_DOCSTRINGS = {
    'extract_feature_vectors': '''
extract_feature_vectors:
    Given a source code, compute the 12 source code metrics (class, methods and NLP metrics).

    Example usage:
        $ python3 bug-prediction.py extract_feature_vectors -s <path-to-src>

    flags:
    -s <path-to-src> | --source <path-to-src>:
        The path to the source code.
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)



