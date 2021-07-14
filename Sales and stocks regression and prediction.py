#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


# In[2]:


Data = pd.read_csv(r"C:\Users\amarn\Desktop\datasets_205965_451952_supermarket_sales - Sheet1.csv")
print(Data)
Data.head()


# In[80]:


Data.shape
Data.info()
Data.describe()


# In[81]:


# Checking Null values
Data.isnull().sum()*100/Data.shape[0]
# There are no NULL values in the dataset, hence it is clean.


# In[82]:


# Outlier Analysis
fig, axs = plt.subplots(3, figsize = (5,5))
plt1 = sns.boxplot(Data['Unit price'], ax = axs[0])
plt2 = sns.boxplot(Data['gross income'], ax = axs[1])
plt3 = sns.boxplot(Data['Rating'], ax = axs[2])
plt.tight_layout()


# In[83]:


sns.boxplot(Data['Tax 5%'])
plt.show()


# In[5]:


# Let's see the correlation between different variables.
sns.heatmap(Data.corr(), cmap="Pastel2", annot = True)
plt.show()


# In[85]:


sns.pairplot(Data, x_vars=['Unit price', 'gross income', 'Tax 5%'], y_vars='Rating', height=4, aspect=1, kind='scatter')
plt.show()


# In[86]:


X = Data['Unit price']
y = Data['Rating']


# In[87]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7, test_size = 0.3, random_state = 100)


# In[88]:


# Let's Train dataset

X_train.head()


# In[89]:


y_train.head()


# In[90]:


import statsmodels.api as sm


# In[91]:


# Add a constant to get an intercept
X_train_sm = sm.add_constant(X_train)

# Fit the resgression line using 'OLS' 
lr = sm.OLS(y_train, X_train_sm).fit()


# In[92]:


# Print the parameters, i.e. the intercept and the slope of the regression line fitted
lr.params


# In[93]:


# Performing a summary operation lists out all the different parameters of the regression line fitted
print(lr.summary())


# In[94]:


plt.scatter(X_train, y_train)
plt.plot(X_train, 6.948 + 0.054*X_train, 'r')
plt.show()


# In[95]:


# sales prediction
y_train_pred = lr.predict(X_train_sm)
res = (y_train - y_train_pred)


# In[96]:


fig = plt.figure()
sns.distplot(res, bins = 15)
fig.suptitle('Errors', fontsize = 15)                  # Plot heading 
plt.xlabel('y_train - y_train_pred', fontsize = 15)         # X-label
plt.show()


# In[97]:


plt.scatter(X_train,res)
plt.show()


# In[98]:


# Add a constant to X_test
X_test_sm = sm.add_constant(X_test)

# Predict the y values corresponding to X_test_sm
y_pred = lr.predict(X_test_sm)


# In[99]:


y_pred.head()


# In[100]:


from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# In[101]:


#Returns the mean squared error; we'll take a square root
np.sqrt(mean_squared_error(y_test, y_pred))


# In[102]:


r_squared = r2_score(y_test, y_pred)
r_squared


# In[103]:


plt.scatter(X_test, y_test)
plt.plot(X_test, 6.948 + 0.054 * X_test, 'r')
plt.show()


# In[ ]:




