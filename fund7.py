# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 21:54:17 2022

@author: alexa
"""
import pandas as pd
import numpy as np
from pathlib import Path


#Creating a dataframe from the vCA aggregated file (vCA Aggregated tab), which was downloaded beforehand into a local folder as a .xlsx file
aggregated_df = df = pd.read_excel ('vCA Aggregated - Fund 7.xlsx', sheet_name='vCA Aggregated')
aggregated_df.set_index("id",inplace=True,drop=True)


def weighted_score (filtered, good, excellent, total):
    """
    filtered : number of Filtered Out reviews an assessment received ("Filtered" column)
    good : number of Good reviews an assessment received ("Good" column)
    excellent : number of Excellent reviews an assessment received ("Excellent" column)     
    total : total number of reviews and assessment received ("# of vCAs Reviews" column)
    
    Returns :
    this functions returns the weighted score for each assessment by translating
    each qualitative score of Excellent, Good and Filtered out into a numerical
    score as w_excell, w_good and w_filter respectevely (w stands for weight)
    """
    w_filter = 0
    w_good = 1
    w_excell = 3
    return (((filtered/total)*w_filter)+((good/total)*w_good)+((excellent/total)*w_excell))

#creates a new column in the aggregated dataframe with the weighted average score for each assessment using the weighted_score function
aggregated_df['weighted av. score'] = aggregated_df.apply(lambda x:
                                                          weighted_score(x['Filtered Out'], x['Good'], x['Excellent'], x['# of vCAs Reviews']), axis=1)

    
def merge_results (filtered, good, excellent):
    """
    filtered : "Result Filtered Out" column of aggregated_df
    good : "Result Good column" column of aggregated_df 
    excellent : "Result Excellent" column of aggregated_df 

    Returns : 
    0 if assessment was Filtered Out ("Result Filtered Out" column marked with an x)
    1 if assessment was reviewed as Good ("Result Good" column marked with an x)
    3 if assessment was reviwed as Excellent ("Result Excellent" column marked with an x)   
    """
    
    if filtered == 'x':
        return 0
    elif good == 'x':
        return 1
    elif excellent == 'x':
        return 3
    else:
        return np.nan

#creates a new column in the aggregated dataframe that condenses the final review score of each assessment into 1 column (instead of 3)
aggregated_df['Final Score'] = aggregated_df.apply(lambda x:
                                    merge_results(x['Result Filtered Out'], x['Result Good'], x['Result Excellent']), axis=1)
aggregated_df.drop(columns=['Result Excellent', 'Result Good', 'Result Filtered Out'])
    
    

"""The section below deals with the indivual vCA sheets. Currentely the individual vCA sheets are downloaded 1 by 1 to a local folder into a .csv format.
The links to the individual vCA sheets can be found in the "Veteran Comunity Advisors" tab of the aggregated file. Unfortunately the name of the individual vCA sheets 
does not match with the name of the vCA, so the currentely i am matching these manually in a new file called "filenames.csv". This file contains 4 columns:
Order, vCA Name, vCA Abreviation and Filename.
These manual steps could be removed by reading directly from the google sheet links provided in the aggregated file. This approach is being investigated
"""
vca_folder = Path('individual_vCAs') #folder location where vCA sheets were downloaded into  
filenames_df = pd.read_csv ('filenames.csv') #creating a dataframe from the filename.csv file created manually (see description above)
filenames_df.set_index('Order',inplace=True,drop=True)

#filename_df is converted into a list which is faster and easier to iterate over
list_of_vCAs = [filenames_df['Name'].tolist(), filenames_df['Abreviation'].tolist(), filenames_df['Filename'].tolist()]

#this list will capture the summarized results of the deviation calculation 
list_mean_deviation_per_vCA = [filenames_df['Name'].tolist(), filenames_df['Abreviation'].tolist(),[]]


#iterating over all vCAs by name     
for name in list_of_vCAs[0]:
    index = list_of_vCAs[0].index(name)
    abreviation = list_of_vCAs[1][index]
    filename = list_of_vCAs[2][index]
    
    #creates a dataframe from the individual vCA sheet and condenses the score given of Excellent, Good or Filtered Out into 1 column (instead of 3)
    individual_df = pd.read_csv(vca_folder/filename)
    individual_df.set_index("id",inplace=True,drop=True)
    individual_df['Result'] = individual_df.apply(lambda x:
                                        merge_results(x['Filtered Out'], x['Good'], x['Excellent']), axis=1)
    
    #in this section i deal with transfering data from the individual_df (individual vCA data) into the aggregated_df
    vca_deviation = abreviation + ' deviation'
    vca_deviation_abs = abreviation + ' deviation abs' 
    aggregated_df[abreviation], aggregated_df[vca_deviation], aggregated_df[vca_deviation_abs] = np.nan, np.nan, np.nan
    
    #this second loop transfers the data from the individual dataframe into the aggregated dataframe
    for index, row in aggregated_df.iterrows():    
        #index = "id" column (the assessment id)
        if index in individual_df.index:
            aggregated_df.loc[index,name] = individual_df.loc[index, "Result"] 
            aggregated_df.loc[index,vca_deviation] = individual_df.loc[index, "Result"] - aggregated_df.loc[index,"weighted av. score"]
            aggregated_df.loc[index,vca_deviation_abs] = abs(individual_df.loc[index, "Result"] - aggregated_df.loc[index,"weighted av. score"])
        else:
            aggregated_df.loc[index,name] = np.nan
    

    list_mean_deviation_per_vCA[2].append(aggregated_df[vca_deviation_abs].mean())


results_folder = Path("results/") #folder location for final results  
aggregated_df.to_csv(results_folder/'aggregated_test_190222.csv') #exports final results into a .csv file
#below a the list_mean_deviation_per_vCA is converted into a dataframe so it can be exported as a.csv
deviation_summary_df = pd.DataFrame({'Name':list_mean_deviation_per_vCA[0], 'Deviation':list_mean_deviation_per_vCA[2] })
deviation_summary_df.to_csv(results_folder/'deviation_summary.csv')


"""
The section below, groups the final results calculated above by Assessor and by Idea Title
"""


by_assessor_df = aggregated_df.groupby("Assessor")['weighted av. score'].mean().reset_index()
by_idea_df = aggregated_df.groupby("Idea Title")['weighted av. score'].mean().reset_index()

for abreviation in list_of_vCAs[1]:
    vca_deviation_column = abreviation + ' deviation' 
    series_assessor = aggregated_df.groupby("Assessor")[vca_deviation_column].mean().reset_index()
    by_assessor_df[vca_deviation_column] = series_assessor[vca_deviation_column]
    
    series_idea = aggregated_df.groupby("Idea Title")[vca_deviation_column].mean().reset_index()
    by_idea_df[vca_deviation_column] = series_idea[vca_deviation_column]

   
by_assessor_df.to_csv(results_folder/'by_assessor.csv')
by_idea_df.to_csv(results_folder/'by_idea.csv')






