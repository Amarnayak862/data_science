#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[24]:


data = pd.read_csv("D:\Mall_Customer.csv")


# In[25]:


data


# In[26]:


df = data.drop(['CustomerID'], axis = 1)


# In[31]:


df


# In[32]:


df.describe()


# In[29]:


df.columns


# In[33]:


df.isnull().sum()


# In[34]:


plt.figure(1, figsize=(15,6))
n = 0
for x in ['Age', 'Annual_income', 'Spending_score']:
    n += 1
    plt.subplot(1, 3, n)
    plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
    sns.distplot(df[x], bins = 20)
    plt.title('Distplot of {}'.format(x))
plt.show()


# In[35]:


plt.figure(figsize=(15,5))
sns.countplot(y = 'Gender', data = df)
plt.show()


# In[36]:


plt.figure(1, figsize=(15,7))
n = 0
for cols in ['Age', 'Annual_income', 'Spending_score']:
    n += 1
    plt.subplot(1, 3, n)
    sns.set(style="whitegrid")
    plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
    sns.violinplot(x = cols, y = 'Gender', data = df)
    plt.ylabel('Gender' if n==1 else '')
    plt.title('violinplot')
plt.show()


# # Age Category

# In[38]:


age_18_25 = df.Age[(df.Age >= 18) & (df.Age <= 25)]
age_26_35 = df.Age[(df.Age >= 26) & (df.Age <= 35)]
age_36_45 = df.Age[(df.Age >= 36) & (df.Age <= 45)]
age_46_55 = df.Age[(df.Age >= 46) & (df.Age <= 55)]
age_55above = df.Age[(df.Age >= 56)]

agex = ["18-25", "26-35", "36-45", "46-55", "55+"]
agey = [len(age_18_25.values),len(age_26_35.values),len(age_36_45.values),len(age_46_55.values),len(age_55above.values)]

plt.figure(figsize=(15,6))
sns.barplot(x=agex, y=agey, palette="mako")
plt.title("Number of customers and Ages")
plt.xlabel("Age")
plt.ylabel("Number of customers")
plt.show()


# In[40]:


sns.relplot(x = "Annual_income", y = "Spending_score", data=df)


# # Spending Score

# In[43]:


ss_1_20 = df["Spending_score"][(df["Spending_score"] >= 1) & (df["Spending_score"] <= 20)]
ss_21_40 = df["Spending_score"][(df["Spending_score"] >= 21) & (df["Spending_score"] <= 40)]
ss_41_60 = df["Spending_score"][(df["Spending_score"] >= 41) & (df["Spending_score"] <= 60)]
ss_61_80 = df["Spending_score"][(df["Spending_score"] >= 61) & (df["Spending_score"] <= 80)]
ss_81_100 = df["Spending_score"][(df["Spending_score"] >= 81) & (df["Spending_score"] <= 100)]
                                
ssx = ["1-20", "21-40", "41-60", "61-80", "81-100"]
ssy = [len(ss_1_20.values), len(ss_21_40.values), len(ss_41_60.values), len(ss_61_80.values), len(ss_81_100.values)]

plt.figure(figsize=(15,6))
sns.barplot(x=ssx, y=ssy, palette="rocket")
plt.title("Spending_score")
plt.xlabel("Score")
plt.ylabel("Number of customers Having the Score")
plt.show()


# # Annual Income

# In[48]:


ai0_30 = df["Annual_income"][(df["Annual_income"] >= 0) & (df["Annual_income"] <= 30)]
ai31_60 = df["Annual_income"][(df["Annual_income"] >= 31) & (df["Annual_income"] <= 60)]
ai61_90 = df["Annual_income"][(df["Annual_income"] >= 61) & (df["Annual_income"] <= 90)]
ai91_120 = df["Annual_income"][(df["Annual_income"] >= 91) & (df["Annual_income"] <= 120)]
ai121_150 = df["Annual_income"][(df["Annual_income"] >= 121) & (df["Annual_income"] <= 150)]

aix = ["$ 0-30,000", "$31,000-60,000", "$61,000-90,000", "$91,000-120,000", "$121,000-150,000"]
aiy = [len(ai0_30.values), len(ai31_60.values), len(ai61_90.values), len(ai91_120.values), len(ai121_150.values)]

plt.figure(figsize=(15,6))
sns.barplot(x=aix, y=aiy, palette="Spectral")
plt.title("Anuual Income")
plt.xlabel("Income")
plt.ylabel("Number of customers")
plt.show()


# In[57]:


X1=df.loc[:, ["Age", "Spending_score"]].values

from sklearn.cluster import KMeans
WCSS = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans.fit(X1)
    WCSS.append(kmeans.inertia_)
plt.figure(figsize=(12,6))
plt.grid()
plt.plot(range(1,11),WCSS, linewidth=2, color="red", marker="8")
plt.xlabel("K Values")
plt.ylabel("WCSS")
plt.show()


# In[61]:


kmeans = KMeans(n_clusters=4)

label = kmeans.fit_predict(X1)

print(label)


# In[62]:


print(kmeans.cluster_centers_)


# In[64]:


plt.scatter(X1[:,0], X1[:,-1], c=kmeans.labels_, cmap='rainbow')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color = 'black')
plt.title('CLuster of Customers')
plt.xlabel('Age')
plt.ylabel('Spending_score')
plt.show()


# In[67]:


X2=df.loc[:, ["Annual_income", "Spending_score"]].values

from sklearn.cluster import KMeans
wcss = []
for k in range(1,11):
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans.fit(X2)
    wcss.append(kmeans.inertia_)
plt.figure(figsize=(12,6))
plt.grid()
plt.plot(range(1,11),wcss, linewidth=2, color="red", marker = "8")
plt.xlabel("K Value")
plt.ylabel("WCSS")
plt.show()


# In[70]:


kmeans = KMeans(n_clusters=5)
label = kmeans.fit_predict(X2)
print(label)


# In[75]:


plt.scatter(X1[:,0], X2[:,1], c=kmeans.labels_,cmap='rainbow')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color='black')
plt.title('Clusters of Customers')
plt.xlabel('Age')
plt.ylabel('Spending_score')
plt.show()


# In[72]:


print(kmeans.cluster_centers_)


# In[73]:


plt.scatter(X2[:,0], X1[:,1], c=kmeans.labels_,cmap='rainbow')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color='black')
plt.title('Clusters of Customers')
plt.xlabel('Annual_income')
plt.ylabel('Spending_score')
plt.show()


# In[76]:


X3=df.iloc[:,1:]

wcss = []
for k in range(1,11):
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans.fit(X2)
    wcss.append(kmeans.inertia_)
plt.figure(figsize=(12,6))
plt.grid()
plt.plot(range(1,11),wcss, linewidth=2, color="red", marker = "8")
plt.xlabel("K Value")
plt.ylabel("WCSS")
plt.show()


# In[77]:


kmeans = KMeans(n_clusters = 5)
label = kmeans.fit_predict(X3)
print(label)


# In[78]:


print(kmeans.cluster_centers_)


# In[80]:


clusters = kmeans.fit_predict(X3)
df["label"] = clusters

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(df.Age[df.label == 0], df["Annual_income"][df.label == 0], df["Spending_score"][df.label==0], c='blue', s=60)
ax.scatter(df.Age[df.label == 1], df["Annual_income"][df.label == 1], df["Spending_score"][df.label==1], c='red', s=60)
ax.scatter(df.Age[df.label == 2], df["Annual_income"][df.label == 2], df["Spending_score"][df.label==2], c='green', s=60)
ax.scatter(df.Age[df.label == 3], df["Annual_income"][df.label == 3], df["Spending_score"][df.label==3], c='orange', s=60)
ax.scatter(df.Age[df.label == 4], df["Annual_income"][df.label == 4], df["Spending_score"][df.label==4], c='purple',s=60)

ax.view_init(30,185)

plt.xlabel("Age")
plt.ylabel("Annual_income")
ax.set_zlabel('Spending_score')
plt.show()

