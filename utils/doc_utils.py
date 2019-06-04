from utils.misc import indent

DOCSTRING = '''
2019-proj2-bug-prediction
by Gustavo Graziani

Commands:
{extract_feature_vectors}
{label_feature_vectors}
{train_classifiers}
{evaluation}

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
''',
    'label_feature_vectors': '''
label_feature_vectors:
    Given a feature vector and a list of buggy classes, it adds a buggy label to each row, where
    "1" stands for "buggy" and "0" for "not-buggy".

    Example usage:
        $ python3 bug-prediction.py label_feature_vectors -fv <path-to-feature-vector> -b <path-to-buggy-classes-folder>

    flags:
    -fv <path-to-feature-vector> | --feature_vector <path-to-feature-vector>
        The path to the feature vector.
        
    -b <path-to-buggy-classes-folder> | --buggy_classes <path-to-buggy-classes-folder>
        The path to the folder containing the buggy classes.
''',
    'train_classifiers': '''
train_classifiers:
    Given a labeled feature vector, it train the classifiers, prints the averages, save the result to a csv and to a plot.

    Example usage:
        $ python3 bug-prediction.py train_classifiers -lfv <path-to-label-feature-vector>

    flags:
    -lfv <path-to-label-feature-vector> | --label_feature_vector <path-to-label-feature-vector>
        The path to the labeled feature vector.
''',
    'evaluation': '''
evaluation:
    Given a labeled feature vector, it evaluates the classifiers using various methods.

    Example usage:
        $ python3 bug-prediction.py train_classifiers -lfv <path-to-label-feature-vector>

    flags:
    -lfv <path-to-label-feature-vector> | --label_feature_vector <path-to-label-feature-vector>
        The path to the labeled feature vector.
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)



