---

layout: poster

title: 基于GBDT算法的不完全对称信息下的客户授信评估问题

date: 2018-06-02 16:32:49

tags: [XGBoost,Python,Math_model]

---

## 这是数学建模校赛的题目，两个人写建模论文确实太累了

本文针对不完全对称信息下的客户授信评估问题，利用`GBDT(Gradient Boosting Decesion Tree)`梯度提升决策树算法等方法，综合运用了`Python、Xgboost、Matlab`等软件建立了授信额度估算模型和客户预测违约模型，定量分析了在完整数据以及数据缺失情况下的模型效果，并向公司管理层提出了关于授信额度估算的分析与建议。
<!--more-->
#### 针对问题1,

 对于28个自变量的规律分析，我们首先分析自变量和目标因变量，以确定自变量参数与因变量客户违约的关联性。通过绘制自变量和两个因变量之间Pearson相关系数的热力图像，观察得到自变量和因变量的统计关系规律。为了对违约分类进行预测，利用GBDT（Gradient Boost decision tree）算法建立二分类模型，对回归树得到的连续值设定阈值，映射为离散的0-1两点；同时，我们注意到样本正负样本的显著不平衡性，通过欠采样反法，从大量的正样本中选取一定的样本数量，使得正反样本比例接近，再多次进行算法的学习。最后，求出模型的AUC值以评价此模型的准确性。

#### 针对问题2，

对于授信额度估算模型，利用GBDT算法建立回归预测模型。在模型的建立中，分析得到对信用额度Amount 影响权值最高的特征参数，并分析这些参数与信用额度的分布关系。根据建立的二分类模型，预测Class条目未知的客户的违约情况。最后，根据均方根误差值（RMSE）评判GBDT回归预测模型的准确性，并给出对未知客户的违约情况预测。

#### 针对问题3，

在数据有残缺的情形下，我们建立如下的模型，构建参数重要度指标，将缺失的特征参数分为两类： 重要度低于阈值α的特征（即对信用额度影响较小的特征）数值，可以利用其他客户的平均值替代，通过对比实际参数值所得到的信用额度，可以发现此方法与实际值的偏差较小。若特征参数为问题二中得到的重要参数，若利用其他客户的平均值替代 ，根据测试数据，发现偏差值较大。

#### 问题4，

我们总结了本文的工作内容，并撰写了分析报告，归纳展示了本文主要工作。

####关键字 :

------

> * GBDT 

> * XGBoost

> * 数据分析

> * 机器学习
------

```

Xgboost: 最初开发的实现可扩展，计算速度快，模型表现好，分布式 gradient boosting (GBDT, GBRT or GBM) 算法的一个库。

GBDT: gradient boosting decision tree梯度提升决策树算法，既可以用于分类也可以用于回归问题中。

Gradient Boosting: Gradient boosting 是 boosting 的其中一种方法

所谓 Boosting ，就是将弱分离器 f_i(x) 组合起来形成强分类器 F(x) 的一种方法。

所以 Boosting 有三个要素：

​    • A loss function to be optimized：例如分类问题中用 cross entropy，回归问题用 mean squared error。

​    • A weak learner to make predictions： 例如决策树。

​    • An additive model：将多个弱学习器累加起来组成强学习器，进而使目标损失函数达到极小。

梯度提升Gradient boosting ：就是通过加入新的弱学习器，来努力纠正前面所有弱学习器的残差，最终这样多个学习器相加在一起用来进行最终预测，准确率就会比单独的一个要高。之所以称为 Gradient，是因为在添加新模型时使用了梯度下降算法来最小化的损失。

决策树Decision tree: 是一个树结构（可以是二叉树或非二叉树），既可以作为分类算法，也可以作为回归算法。其每个非叶节点表示一个特征属性上的测试，每个分支代表这个特征属性在某个值域上的输出，而每个叶节点存放一个类别。使用决策树进行决策的过程就是从根节点开始，测试待分类项中相应的特征属性，并按照其值选择输出分支，直到到达叶子节点，将叶子节点存放的类别作为决策结果。

```

#### 图片

![d.png](https://i.loli.net/2018/06/02/5b12577d73f94.png)

![f.png](https://i.loli.net/2018/06/02/5b12577d841c8.png)

![c.png](https://i.loli.net/2018/06/02/5b12577d85a38.png)

![e.png](https://i.loli.net/2018/06/02/5b12577da910f.png)

![a.png](https://i.loli.net/2018/06/02/5b12577ed9159.png)

![b.png](https://i.loli.net/2018/06/02/5b12577ede731.png)



#### code

```python
# Load in our libraries
import pandas as pd
import numpy as np
import re
import sklearn
import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

# import plotly.offline as py
#py.init_notebook_mode(connected=True)
#import plotly.graph_objs as go
#import plotly.tools as tls

import warnings
warnings.filterwarnings('ignore')

# Going to use these 5 base models for the stacking
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, 
                              GradientBoostingClassifier, ExtraTreesClassifier)
from sklearn.svm import SVC
from sklearn.cross_validation import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score,roc_curve,roc_auc_score
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.grid_search import GridSearchCV
```

```python
train = pd.read_csv('D:\Data\File\\train.csv')
test = pd.read_csv('D:\Data\File\\test.csv')

# Store our passenger ID for easy access
#PassengerId = train['']
print(train.shape)
train.tail(3)
# Load in the train and test datasets
train = pd.read_csv('D:\Data\File\\train.csv')
test = pd.read_csv('D:\Data\File\\test.csv')

# Store our passenger ID for easy access
#PassengerId = train['']
print(train.shape)
test.tail(3)

Test=test.drop(['Class','Amount','ID','Time'],axis=1)
type(train)


colormap=plt.cm.RdBu
plt.figure(figsize=(32,32))
plt.title('Pearson Correlation of Features', y=1.05, size=32)
sns.heatmap(tem.astype(float).corr(),linewidths=0.2,vmax=1.0, 
            square=True, cmap=colormap, linecolor='white', annot=True)
plt.savefig("heatCorr.png")


Train=train.head(12800)
Train=Train.append(train.tail(12800))
sTrain=Train.drop(['Class','Amount','ID','Time'],axis=1)
yTrain=Train['Class']
test_size=0.25
seed=7
a_train,a_test,b_train,b_test=train_test_split(sTrain,yTrain,test_size=test_size,random_state=seed)
print(a_test.shape)
print(b_test.shape)

#xgboost 有封装好的分类器和回归器，可以直接用 XGBClassifier 建立模型
#这里是 XGBClassifier 的文档：
#http://xgboost.readthedocs.io/en/latest/python/python_api.html#module-xgboost.sklearn
a_test
model=xgb.XGBClassifier( #learning_rate = 0.02,
 n_estimators= 2550,
 max_depth= 5,
 min_child_weight= 2,
 #gamma=1,
 gamma=0.9,                        
 subsample=0.7,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread= -1,
silent=0,
eta=0.1,
eval_metric='auc',
scale_pos_weight=1)
eval_set=[(a_test,b_test)]
model.fit(a_train,b_train, early_stopping_rounds=15, eval_metric="auc", eval_set=eval_set, verbose=True)
b_predict=model.predict_proba(a_test)
#评价模型在测试集上的表现，也可以输出每一步的分,那么它会在每加入一颗树后打印出 logloss
b_predict

xgb.plot_importance(model,max_num_features=28,grid=False)
plt.savefig('class_feature.png')
#for it in b_predict:
 #   print(it)
    
fpr_sk1,tpr_sj1,threshold=roc_curve(b_test,b_predict[0:3000,1],drop_intermediate=False)
plt.plot(fpr_sk1,tpr_sj1)
plt.savefig('roc.png')


var = 'V4'
%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)
var = 'V12'
%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)
var = 'V14'
%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)
var = 'V7'
%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)
var = 'V11'
%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)
var = 'V17'
%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)
var = 'V1'

%time data = pd.concat([train['Amount'], train[var]], axis=1)
data.plot.scatter(x=var, y='Amount', ylim=(0,7200));
st=str(var)+'.png'
plt.savefig(st)


#scatterplot
sns.set()
cols = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7','V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14']
sns.pairplot(train[cols], size = 2.5)
plt.show();
plt.savefig('pairPlot.png')

Train=train.head(50000)
#Train=Train.append(train.tail(8000))
sTrain=Train.drop(['Class','ID','Time'],axis=1)
yTrain=Train['Amount']
test_size=0.125
seed=7
a_train,a_test,b_train,b_test=train_test_split(sTrain,yTrain,test_size=test_size,random_state=seed)

# Regression by XGBoost
%timeit 
bst=xgb.XGBRegressor(seed=1850,max_depth= 5,
min_child_weight= 1,
 #gamma=1,
                          
                
subsample=0.8,
colsample_bytree=0.8,

silent=0,
eta=0.1,
eval_metric='rmse',
 cale_pos_weight=1)

bst.fit(a_train,
b_train,
verbose=True, #learning_rate = 0.02,
)
preds=bst.predict(a_test)
preds


# 调整参数
#xgb1=xgb.XGBRegressor(base_sc)
M=28400
train = pd.read_csv('D:\Data\File\\train.csv')
test = pd.read_csv('D:\Data\File\\test.csv')
Train=train.drop(['Class','Amount','ID','Time'],axis=1)
sTrain=Train.tail(M)
yTrain=train['Amount']
ytrain=yTrain.tail(M)
test_size=0.25
seed=1850
x_train,x_test,y_train,y_test=train_test_split(sTrain,ytrain,test_size=test_size,random_state=seed)
param={
    #'max_depth':[2,3,4,5],
   # 'min_child_weight':[1,2,3,4,5]
    #'learning_rate':[0.01,0.04,0.08,0.16, 0.2],
   # 'max_delta_step':[0,0.2,0.4,0.6,0.8,1]

}
gsearch=GridSearchCV(estimator=xgb.XGBRegressor(
    max_depth=5,
    min_child_weight=1,
    max_delta_step=0,
    n_estimator=750,
    seed=1850,
    silent=True,
    learning_rate=0.16,
),
param_grid= param,scoring='neg_mean_squared_error' ,cv=5 )
#gsearch.fit(Train,train['Amount'])
model=gsearch.fit(x_train,y_train)
gsearch.grid_scores_,gsearch.best_params_,gsearch.best_score_,gsearch.best_estimator_,gsearch.cv,gsearch.verbose,

f2 = plt.figure(2)  
#idx_1 = find(label==1)  
p1 = plt.scatter(x,preds, marker = '*', color = 'm', label='1', s = 30)  
#idx_2 = find(label==2)  
#p2 = plt.scatter(x,b_test, marker = 'o', color = 'c', label='2', s = 30)  
plt.savefig('2-1.png')

xgb.plot_tree(booster=model,num_trees=16)
plt.savefig("tree.png",dpi=720)

n=79
x=range(0,n,1)
plt.plot(x,pr[:n],'-r')
plt.plot(x,y_test[:n],'-g')
plt.savefig('ppppp.png')
```

