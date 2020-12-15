import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures

def getColumnsList(df):
    return df.columns.tolist()

def getNaNIndex(df):
    df_null=df.isnull().unstack()
    return df_null[df_null]

def encodeColumns(df,colToEncode=[]):
    encoder=LabelEncoder()
    if colToEncode!=[]:
        for col in colToEncode:
            df[col]=encoder.fit_transform(df[col])
    return df

def transformNan(df): 
    imptr=SimpleImputer(missing_values=np.NaN, strategy='mean')

    for col in  df.select_dtypes(exclude='object'):
        imptr.fit(df[col].values.reshape(-1,1))
        df[col]=imptr.transform(df[col].values.reshape(-1,1))[0:,0]

    return df

def createTestAndTrainSet(X,Y):
    
    x_test, x_app, y_test, y_app = train_test_split(X,Y,test_size=0.8,random_state=3)

    return x_test, x_app, y_test, y_app

def scaleFeatures(df,colToScale):

    df[colToScale]=pd.DataFrame(StandardScaler().fit_transform(df[colToScale]))
    return df


def getDataSet(name,sep=","):

    df=pd.read_csv(name, sep=sep)
    return df