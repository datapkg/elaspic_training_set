## Pipeline

### Prepare data

#### [elaspic_standalone](/notebooks/elaspic_standalone.ipynb)
  
Calculate ELASPIC features for the core and interface training sets, using the ELASPIC standalone pipeline.

#### [elaspic_database_core](/notebooks/elaspic_database_core.ipynb)

Calculate ELASPIC features for core training sets, using the ELASPIC database pipeline.

#### [elaspic_database_interface](/notebooks/elaspic_database_interface.ipynb)

Calculate ELASPIC features for interface training sets, using the ELASPIC database pipeline.

#### [load_data](/notebooks/load_data.ipynb)

Prepare and combine all training, validation and test data into a single file for ML.

#### [data_statistics](/notebooks/data_statistics.ipynb)

Compute basic statistics regarding the training and validation datasets.


### Train ELASPIC

#### [machine_learning](/notebooks/machine_learning.ipynb)

Train the ELASPIC core and interface predictors.


### Validation

#### [validation](/notebooks/validation.ipynb)

Validate ELASPIC core and interface predictors on the validation and test datasets.

#### [validation_cancer](/notebooks/validation_cancer.ipynb)

Use ELASPIC scores to predict whether a mutation is a cancer driver or a cancer passenger.


### Other

#### [elaspic_statistics](/notebooks/elaspic_statistics.ipynb)

Analysing our homology modelling and mutation coverage for the human proteome.

#### [elaspic_to_calculate](/notebooks/elaspic_to_calculate.ipynb)

Get a list of mutations from the validation and test datasets that remain to be calculated.

