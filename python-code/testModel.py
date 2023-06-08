#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:48:43 2023

@author: cmau
"""


import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

def testModel(testImages,testBasisFun,testTarget,V,beta,W,trainBasisFunMean,trainBasisFunStd, priorVarTarget=1,priorMeanTarget=0):

    targetTrainMean = trainBasisFunMean[0]
    targetTrainStd = trainBasisFunStd[0]
    nLatentVars = np.shape(V)[1]
    nVoxels = np.shape(V)[0]
    
    w_star = np.reshape(W[:,0],(nVoxels,1))
    
    #diag_betas=spdiags(beta,0,n_voxels,n_voxels);
    
    SigmaZ_inv=np.eye(nLatentVars)+np.dot(np.transpose(V),beta*V)
    SigmaZ=np.linalg.inv(SigmaZ_inv)
   
    
    DeltaTimesWstar = beta*w_star
    aux=np.dot(np.transpose(V),beta*w_star)
    posteriorVarTarget=1/(1/priorVarTarget+np.dot(np.transpose(w_star),beta*w_star)-np.linalg.multi_dot((np.transpose(aux),SigmaZ,aux)))
    
    
   
    gap=np.transpose(testImages)-np.dot(W[:,1:],np.transpose(testBasisFun[:,1:]))
    aux2=np.dot(np.transpose(V),beta*gap)
    standTargetPredictions=posteriorVarTarget*np.transpose((np.dot(np.transpose(beta*w_star),gap)-np.linalg.multi_dot((np.transpose(aux),SigmaZ,aux2))))
    
    
    #take predictions back to the original target space
    targetPredictions=standTargetPredictions*targetTrainStd+targetTrainMean
    
    #compute correlation and error
    correlation=np.corrcoef(np.transpose(testTarget),np.transpose(targetPredictions))[0,1]
    RMSE=np.sqrt(mean_squared_error(testTarget,targetPredictions))
    MAE=mean_absolute_error(testTarget,targetPredictions)
   
    

    print('correlation : ', correlation, '\n')
    print('RMSE : ', RMSE, '\n')
    print('MAE : ', MAE, '\n')
    print('\n')

    # if showFigures
        
    #     figure, scatter(test_target,targetPredictions)
    #     hold on
    #     plot(test_target,test_target)
    #     xlabel('true score')
    #     ylabel('predicited score')
    #     title('test predictions')
    #     hold off
    
    return targetPredictions,correlation,MAE,RMSE