# DriverSub-SVM
DriverSub-SVM is a model, which innovatively integrates patient-specific and global driver genes with the OAO-MSVM algorithm.The aim is to enhance the accuracy and specificity of cancer subtype classification, thereby opening promising avenues for the advancement of personalized cancer medicine. 

The application of DriverSub-SVM primarily occurs within the Python environment. Meanwhile, the code for KEGG pathway analysis is executed in the R environment.
Install the DriverSub-SVM requied:

1.Initially, the data obtained is preprocessed using the code provided in the DataCode directory. 
The processed data is then stored in the Data directory, thereby facilitating subsequent model training.

2.run the model_training_cross.py in the Code directory, obtain the average results of each evaluation metric after conducting k-fold cross-validation. 
Subsequently, run the second_selected_gene.py to acquire the data required for subsequent KEGG pathway analysis, along with the data for computing SHAP values.

3.run the KEGG_analysis.R in the R environment.

4.run the (SHAP subtype.ipynb) in the Jupyter Notebook.

Because the BRCA dataset has a larger sample size, we conducted 10-fold cross-validation. 
In contrast, due to the smaller sample sizes of the COAD and THCA datasets, we chose to use 5-fold cross-validation.
