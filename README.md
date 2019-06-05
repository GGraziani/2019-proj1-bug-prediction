# 2019-proj2-bug-prediction

### Documentation

For the general documentation run:

    $ python3 bug_prediction.py

For details about each command or instructions on "how to run", run:

    $ python3 bug_prediction.py <command>

### Example usage:

- **Pre-processing**:  

    - Extracting the feature vector
    
        ```bash
        $ python3 bug_prediction.py extract_feature_vectors -s res/defects4j/tmp/src/com/google/javascript/jscomp/
        ```
    
    - Labeling the feature vector
    
        ```bash
        $ python3 bug_prediction.py label_feature_vectors -fv res/feature_vectors/feature_vector-1559747305485.csv -b res/defects4j/framework/projects/Closure/modified_classes
        ```
    
- **Train Classifiers**:
  
   ```bash
   $ python3 bug_prediction.py train_classifiers -lfv res/labeled_feature_vectors/label_feature_vector-1559747305485.csv
   ```
   
- **Evaluation**:

    ```bash
    $ python3 bug_prediction.py train_classifiers -lfv res/labeled_feature_vectors/label_feature_vector-1559747305485.csv
    ```