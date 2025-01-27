# Interpretable-subject-level-prediciton

In this repository, we present a model for image-based single-subject prediction that is inherently interpretable. We provide both the Matlab and the Python version of the code. The repository does not contain a pre-trained model, but it can be used to train a model on your own data. Details about the model can be found in:


**Accurate and explainable image-based prediction using a lightweight generative model**. Mauri, C., Cerri, S., Puonti, O., Mühlau, M. and Van Leemput, K., 2022. In ‘International Conference on Medical Image Computing and
Computer-Assisted Intervention’, Springer, pp. 448–458. https://link.springer.com/chapter/10.1007/978-3-031-16452-1_43

**A Lightweight Generative Model for Interpretable Subject-level Prediction**. Mauri, C., Cerri, S., Puonti, O., Mühlau, M. and Van Leemput, K., 2023. arXiv preprint arXiv:2306.11107
https://arxiv.org/pdf/2306.11107.pdf


## Installation

1. Clone this repository

2. For the Python code, create a virtual environment (e.g. with conda) and install the required packages:

```
conda create -n gen_env python=3.8 scipy nibabel matplotlib hdf5storage scikit-learn -c anaconda -c conda-forge
```


## Preprocessing

- the images needs to be nonlinearly registered to a common space. This can be done e.g. using Freesurfer.

- the experiments in the paper have been performed with downsampled images. 

## Training

### Python
You can train the model on your own data with the following command:


```
python ./Python_code/runTraining.py -nLat <LatentValues> [-sp </path/to/save/model> -n <nameOfSavedModel> -dp </path/to/training/data> -th <threshold_value> -fig ]
```

where:

- ```-nLat``` or ```--nLatentValues``` specifies all the values for the number of latent variables that you want to try. E.g. -nLat 20,50,70,100
- ```-sp``` or ```--savePath``` (optional) specifies the path where the trained model is saved, default="."
- ```-n``` or ```--nameSavedModel``` (optional) specifies the name given to the trained model, default="trainedModel"
- ```-dp``` or ```--dataPath``` (optional) specifies tha folder containing the training data, default=".", see below for requirements on the data format
- ```-th``` or ```--maskThreshold``` (optional) specifies the threshold to use for masking out the background in images before trianing the model. The threshold is applied to the average volume scaled by its maximum. default=0.01
- ```-fig``` or ```--showFigures``` (optional): to display figures 


The code assumes that training data are provided in the following format: 
- trainAge.npy is a numpy array of size (# of subjects, 1) with age of all training subjects;
- trainImages.npy is 4D numpy array of size (# of subjects, image dimension 1, image dimension 2, image dimension 3) with images of all training subjects (nonlinearly registered to a common space).


The code saves a pickle file containing the model with all the specified number of latent variables.

NOTE: the Python code is now slower than the Matlab version, but it will be updated.

### Matlab
You can train the model on your own data with the following command:
```
cd Matlab_code
matlab -batch "runTraining(<LatentValues>,'dataPath',</path/to/training/data>,'savePath',</path/to/save/model>,'nameSavedModel',<nameOfSavedModel>,'maskThreshold',<threshold_value>,'showFigures',<boolean_to_show_figures>)"
```

Or from the GUI:
```
cd Matlab_code
runTraining(<LatentValues>,'dataPath',</path/to/training/data>,'savePath',</path/to/save/model>,'nameSavedModel',<nameOfSavedModel>,'maskThreshold',<threshold_value>,'showFigures',<boolean_to_show_figures>)
```
where:

- ```<LatentValues>``` specifies all the values for the number of latent variables that you want to try. E.g. [20,50,70,100]
- ```</path/to/save/model>``` (optional) specifies the path where the trained model is saved, default='.'
- ```<nameOfSavedModel>``` (optional) specifies the name given to the trained model, default='trainedModel'
- ```</path/to/training/data>``` (optional) specifies the folder containing the training data, default='.', see below for requirements on the data format
- ```<threshold_value>``` (optional) specifies the threshold to use for masking out the background in the images before trianing the model. The threshold is applied to the average volume scaled by its maximum. default=0.01
- ``` <boolean_to_show_figures>``` (optional) specifies if figures are displayed when running, default=true



The code assumes that training data are provided in the following format: 
- trainAge.mat is an array of size (# of subjects, 1) with age of all training subjects;
- trainImages.mat is 4D array of size (# of subjects, image dimension 1, image dimension 2, image dimension 3) with images of all training subjects (nonlinearly registered to a common space).

The code saves a .mat file containing the model with all the specified number of latent variables


## Validation and testing

### Python

We can apply the models that we previously trained with different numbers of latent variables to a validation set, to select the optimal number of latent variables. This can be done with:

```
python ./Python_code/runValidation.py  [-mp </path/to/saved/model> -n <nameOfSavedModel> -dp </path/to/validation/data>]
```
where:

- ```-mp``` or ```--modelPath``` (optional) specifies the path where the trained model is saved, default="."
- ```-n``` or ```--nameSavedModel``` (optional) specifies the name of the pickle file we saved after training, containing the model with all the specified number of latent variables, default="trainedModel.pkl"
- ```-dp``` or ```--dataPath``` (optional) specifies the path to validation data, default=".", see below for requirements on the data format

The code assumes that validation data are provided in the following format: 
- validAge.npy is a numpy array of size (# of subjects, 1) with age of all validation subjects;
- validImages.npy is 4D numpy array of size (# of subjects, image dimension 1, image dimension 2, image dimension 3) with images of all validation subjects (nonlinearly registered to a common space).

The code displays the error metrics on the validation set for all the specified number of latent variables, and save the corresponding information in a pickle file. This can be used to select the optimal number of latent variables.

We are now ready for the final evaluation of the model on a separate test set, using the optimal number of latent variables that we selected. This can be done with:

```
python ./Python_code/runTest.py -nLat <OptimalNumberOfLatentVar> [-mp </path/to/saved/model> -n <nameOfSavedModel> -dp </path/to/test/data> -sp </path/to/save/results>]
```
where:

- ```-nLat``` or ```--nLatent``` specifies the number of latent variables that we want to use for testing (it should be the optimal value selected on the validation set)
- ```-mp``` or ```--modelPath``` (optional) specifies the path where the trained model is saved, default="."
- ```-n``` or ```--nameSavedModel``` (optional) specifies the name of the pickle file we saved after training, containing the model with all the specified number of latent variables, default="trainedModel.pkl"
- ```-dp``` or ```--dataPath``` (optional) specifies the path to test data, default=".", see below for requirements on the data format
- ```-sp``` or ```--savePath``` (optional) specifies the path where the test results are saved, default="."

The code assumes that test data are provided in the following format: 
- testAge.npy is a numpy array of size (# of subjects, 1) with age of all test subjects;
- testImages.npy is 4D numpy array of size (# of subjects, image dimension 1, image dimension 2, image dimension 3) with images of all test subjects (nonlinearly registered to a common space).

The code displays the error metrics on the test set obtained with the final model (the one with the specified optimal number of latent variables) and save the corresponding information in a pickle file.

### Matlab

We can apply the models we previously trained with different numbers of latent variables to a validation set, to select the optimal number of latent variables. This can be done with:

```
cd Matlab_code
matlab -batch "runValidation('dataPath',</path/to/validation/data>,'savePath',</path/to/save/results>,'modelPath',</path/to/saved/model>,'nameSavedModel',<nameOfSavedModel>)"
```

or from the GUI:

```
cd Matlab_code
runValidation('dataPath',</path/to/validation/data>,'savePath',</path/to/save/results>,'modelPath',</path/to/saved/model>,'nameSavedModel',<nameOfSavedModel>)
```

where:

- ```</path/to/save/results>``` (optional) specifies the path where validation results are saved, default='.'
- ```</path/to/saved/model>``` (optional) specifies the path where the trained model is saved, default='.'
- ```<nameOfSavedModel>``` (optional) specifies the name of the .mat file we saved after training, containing the model with all the specified number of latent variables, default='trainedModel.mat'
- ```</path/to/validation/data>``` (optional) specifies the path to validation data, default='.', see below for requirements on the data format

The code assumes that validation data are provided in the following format: 
- validAge.npy is a numpy array of size (# of subjects, 1) with age of all validation subjects;
- validImages.npy is 4D numpy array of size (# of subjects, image dimension 1, image dimension 2, image dimension 3) with images of all validation subjects (nonlinearly registered to a common space).

The code displays the error metrics on the validation set for all the specified number of latent variables, and save the corresponding information in a .mat file. This can be used to select the optimal number of latent variables.

We are now ready for the final evaluation of the model on a separate test set, using the optimal number of latent variables that we selected. This can be done with:

```
cd Matlab_code
matlab -batch "runTest(<OptimalNumberOfLatentVar>,'dataPath',</path/to/test/data ,'savePath',< path/to/save/results>,'modelPath',</path/to/saved/model>,'nameSavedModel',<nameOfSavedModel>)"
```
or from the GUI:

```
cd Matlab_code
runTest(<OptimalNumberOfLatentVar>,'dataPath',</path/to/test/data>,'savePath',</path/to/save/results>,'modelPath',</path/to/saved/model>,'nameSavedModel',<nameOfSavedModel>)
```


where:

- ```<OptimalNumberOfLatentVar>``` specifies the number of latent variables that we want to use for testing (it should be the optimal value selected on the validation set)
- ```</path/to/save/results>``` (optional) specifies the path where test results are saved, default='.'
- ```</path/to/saved/model>``` (optional) specifies the path where the trained model is saved, default='.'
- ```<nameOfSavedModel>``` (optional) specifies the name of the .mat file we saved after training, containing the model with all the specified number of latent variables, default='trainedModel.mat'
- ```</path/to/test/data>``` (optional) specifies the path to test data, default='.', see below for requirements on the data format


The code assumes that test data are provided in the following format: 
- testAge.mat is an array of size (# of subjects, 1) with age of all test subjects;
- testImages.mat is 4D array of size (# of subjects, image dimension 1, image dimension 2, image dimension 3) with images of all test subjects (nonlinearly registered to a common space).

The code displays the error metrics on the test set obtained with the final model (the one with the specified optimal number of latent variables) and save the corresponding information in a .mat file.


## To cite 
Please cite:

**A Lightweight Causal Model for Interpretable Subject-level Prediction**. Mauri, C., Cerri, S., Puonti, O., Mühlau, M. and Van Leemput, K., 2023. arXiv preprint arXiv:2306.11107
https://arxiv.org/pdf/2306.11107.pdf


  

  
