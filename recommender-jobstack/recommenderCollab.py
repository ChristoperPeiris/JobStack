#!/usr/bin/env python
# coding: utf-8

# In[94]:


import re
import pandas as pd
import numpy as np

coding_skill = "ck0"
social_skill = "sk0"
language_skill = "ls0"
program_development = "pd0"
degree = "DID05"
front_end = "fe0"
back_end = "be0"
full_stack = "fs0"
mobile_development = "md0"
web_development = "wd0"
ui_ux = "u0"

rating = pd.read_csv("usersNEW.csv")

main()

def main():
    
    from scipy import sparse
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    new_row = pd.DataFrame({'codingskill':coding_skill, 'socialskill':social_skill, "languageskill":language_skill, 'programdev':program_development, 'degreeid':degree, 'frontenddev':front_end, 'backenddev':back_end,'fullstack':full_stack, 'mobiledev':mobile_development, 'webdev':web_development, 'uiux':ui_ux},index = [0])
     
    rating = pd.concat([new_row,rating]).reset_index(drop = True) 

    rating.fillna(' ',inplace = True)
    
    rating["combined_features"] = rating.apply(combining_features,axis=1)

    cv = CountVectorizer()

    count_matrix = cv.fit_transform(rating["combined_features"]) 

    cosine_similarity = cosine_similarity(count_matrix)

    index = 0

    similar_users = list(enumerate(cosine_similarity[index]))

    sorted_users = sorted(similar_users,key=lambda x:x[1],reverse=True)

    user_list=[]
    i=0
    for user in sorted_users:
        user_list.append(get_user(user[0]))    
        i=i+1
        if i>50:
            break

    companyUserRatingList = []
    companyRatings = pd.read_csv("ratingsNEW.csv")
    df = pd.DataFrame(companyRatings)

    for i in range(len(user_list)-1):
        selected_user = df.loc[df['userid'] == user_list[i+1]]
        for index, row in selected_user.iterrows():
            if any(x.companyID == row['companyid'] for x in companyUserRatingList):
                for gest in companyUserRatingList:
                    if gest.companyID == row['companyid']:
                        sumValue = (gest.sumValue) + row['rating']
                        count = (gest.count) + 1
                        setattr(gest,'sumValue',sumValue)
                        setattr(gest,'count',count)

            else:
                companyDets = UserCompanyRating((row['companyid']),(row['rating']),1)
                companyUserRatingList.append(companyDets)

    company_list=[]
    for couish in companyUserRatingList:    
        company_list.append([couish.companyID,couish.sumValue/couish.count])

    company_sorted_list = sorted(company_list,key=lambda l:l[1],reverse=True)


    data = {'userid':[0],'CID01':[0],'CID02':[0],'CID03':[0],'CID04':[0],'CID05':[0],"CID06":[0],"CID07":[0],"CID08":[0],"CID09":[0],"CID10":[0],"CID11":[0],"CID12":[0],"CID13":[0],"CID14":[0],"CID15":[0],"CID16":[0],"CID17":[0],"CID18":[0],"CID19":[0]}
    dfHUHHH = pd.DataFrame(data)

    alreaadyEntered = []

    for index,row in df.iterrows():
        userid = row['userid']
        compid = row['companyid']
        rating = row['rating']

        if userid in user_list:
            userid = int(re.search(r'\d+', userid).group())
            dfHUHHH.at[userid,compid] = rating

    dfHUHHH = dfHUHHH.drop([0])
    dfHUHHH = dfHUHHH.fillna(0)
    dfHUHHH = dfHUHHH.set_index(['userid'])

    from sklearn.metrics.pairwise import cosine_similarity
    
    dfHUHHH_std =  dfHUHHH.apply(standardize)

    item_similarity = cosine_similarity(dfHUHHH_std.T)

    item_similarity_df = pd.DataFrame(item_similarity,index=dfHUHHH_std.columns,columns=dfHUHHH_std.columns)
    
    companyRatingLast = []
    for company in company_sorted_list:
        for i in range(18):
            if i<9:
                keyMade = "CID0"+str(i+1)
            else:
                keyMade = "CID"+str(i+1)

            similar = get_similar_companies(company[0],company[1])
            similar = similar.get(key = keyMade)

            if any(v.companyIDLast == keyMade for v in companyRatingLast):
                for lastStuff in companyRatingLast:
                    if lastStuff.companyIDLast == keyMade:
                        sumValueLast = lastStuff.sumValueLast + similar
                        countLast = (lastStuff.countLast) + 1
                        setattr(lastStuff,'sumValueLast',sumValueLast)
                        setattr(lastStuff,'countLast',countLast)

            else:
                companyDetsLast = UserCompanyRatingLast(keyMade,similar,1)
                companyRatingLast.append(companyDetsLast)         


    company_list_Last=[]
    for dandan in companyRatingLast:
        company_list_Last.append([dandan.companyIDLast,dandan.sumValueLast/dandan.countLast])

    company_sorted_list_last = sorted(company_list_Last,key=lambda l:l[1],reverse=True)     

    i=0
    print("Top five")
    for companyDisplay in company_sorted_list_last:
        print(companyDisplay)
        i=i+1
        if i>5:
            break



def combining_features(row):
    return(row['codingskill'] + " " +row['socialskill']+ " " +row['languageskill'] + " " +row['programdev']+ " " +row['degreeid']+ " " +row['frontenddev'] + " " +row['backenddev'] + " " +row['fullstack']+ " " +row['mobiledev'] + " " +row['webdev']+ " " +row['uiux'])

def get_user(index):
        return rating[rating.index == index]["userid"].values[0]

              
class UserCompanyRating:
    def __init__(self,companyID,sumValue,count):
        self.companyID = companyID
        self.sumValue = sumValue
        self.count = count   

def standardize(row):
    new_row = (row - row.mean())/(row.max()-row.min())
    return new_row

def get_similar_companies(companyid,rating):
    similar_score = item_similarity_df[companyid]*rating
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score 
    

class UserCompanyRatingLast:
    def __init__(self,companyIDLast,sumValueLast,countLast):
        self.companyIDLast = companyIDLast
        self.sumValueLast = sumValueLast
        self.countLast = countLast
        


# In[ ]:





# In[ ]:





# In[ ]:




