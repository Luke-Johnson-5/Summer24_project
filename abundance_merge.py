#%%
import pandas as pd
import glob
from functools import reduce

files = glob.glob('*.csv')
for file in files: 
    df = pd.read_csv(file) #opens each csv file 
    df = df[["Reference","Relative Abundance"]] #keeps only Reference and Relative Abundance columns   
    df = df.dropna(axis=0) #drops all NA values 
    df["Relative Abundance"] = df.rename(columns={"Relative Abundance": file}, inplace=True) #Renames Relative Abundance column to represent sample name
    df = df.drop('Relative Abundance', axis=1) #drops empty Relative Abundance column
    df.to_csv(file, index=False) #Applies changes to respective csv files  
print("Data Filter and Relative Abundance Reanme Complete")
#%%
frame = [] #create empty frame
for file in files:
    frame.append(pd.read_csv(file)) #open and append all columns for each file together 
    df = reduce(lambda  left,right: pd.merge(left,right,on=['Reference'], how='outer'), frame) #performs a data merge of abundances based off reference genomes 
    df.fillna(0, inplace=True)
    #df = df.transpose() #switches the row and columnn 
print("Data Merge Complete")
#%%
pd.DataFrame.to_csv(df, "master_table.csv")
print("CSV file generation complete")
# %%
