
import glob # use your path
import pandas as pd
from sklearn.cluster import KMeans
import scipy
import numpy as np


def preparedata(file1,zh):
    data2 = pd.DataFrame()
    for i in file1:
        print i
        data = pd.read_csv(i)
        data.drop(['Date','Houseid'], axis=1, inplace=True)
        data = data.fillna(0)
        data1 = pd.DataFrame(data.iloc[zh])
        data2 = pd.concat([data1,data2],axis=1)
    print data2, "data2"
    return data2
        
def kmeansdata(data2):
    da2 = data2.transpose()
    k_mea= KMeans(init='k-means++', n_clusters=47)
#     k_mea= KMeans(k=47)
    barc = k_mea.fit(da2)
    fdf2 = pd.DataFrame(barc.cluster_centers_)
    fdf3 = fdf2.transpose()
    print fdf3, "fdf3 inside function"
    return fdf3

def takeabs(fdf3,actual):
    delta_t = 60
    jh = 1440/delta_t
    ans = []
    for restf in fdf3.columns:
        a = fdf3[restf]
        for shift in range(jh):
            ans.append(scipy.absolute(scipy.roll(a,shift*delta_t) - actual).sum())
    indexloc = ans.index(min(ans))
    pstar = indexloc/jh
    jstar= indexloc%jh
    adf=fdf3[pstar]
    adff=np.roll(adf,jstar)
    adff1=pd.Series(adff)
    print adff1,"pd.Series(adff)"
    return adff1

def mergdat(mergpat,bestpat):
    bestpat = pd.concat([mergpat,bestpat], axis=1)
    return bestpat

files=glob.glob("/test/*.csv")
print(files)
for i in files:
    ite = 0
    words = ['air','dryer','furnace','lights_plugs','refrigerator']
    # for readit in range(0,14400,1440):
    for readit in range(0,2880,1440):
        testf = pd.read_csv(i, skiprows=readit , nrows=1440)
        bestpatmp = pd.DataFrame()
        actual = testf.iloc[:,7]
        print actual
        for  i in words:
            ghj = '*_'+i+'_weekday_out.csv'
            allFiles = glob.glob(ghj)
            data3 = preparedata(allFiles,ite)
            kmpat = kmeansdata(data3)
            bestpat = takeabs(kmpat,actual)
            actual = actual.subtract(bestpat)
            print actual, "actual"
            bestpatmp = mergdat(bestpatmp,bestpat)
        bestpatmp.to_csv('solution_'+i+'.csv', mode='a', index = False, index_label = False, header=False)
        ite += 1

