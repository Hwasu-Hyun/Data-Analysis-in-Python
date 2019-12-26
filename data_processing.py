#!/usr/bin/env python
# coding: utf-8

#-*- encoding: utf8 -*-
import pandas as pd 
import glob
import codecs
import os

### Read files in one folder ###
misumi_call_data = glob.glob('./data/rsv*' )
#print(misumi_call_data)

## Put files in one list ## 
list_call_df= []
for csv_filename in misumi_call_data:
    #print(csv_filename)
    with codecs.open(csv_filename,'r','shift_jis','ignore') as f: 
        df = pd.read_csv(f, error_bad_lines=False)
        list_call_df.append(df)

## Combine list in one dataframe ##        
call_loop_concat = pd.concat(list_call_df)

## Get basic infromation by file/ Read first line by file ##
main_data = call_loop_concat.loc[0].reset_index()
#print(main_data)

## Set timestamp on yyyy/mm/dd ##
main_data['REC_START_TIME'] = main_data['REC_START_TIME'].str.slice(start=0, stop=10)
#print(type(main_data))

## Drop Columns SPEAKER, TEXT ##
main_data = main_data.drop(['SPEAKER', 'TEXT'], axis=1)

## Groupby Voice_id, Speaker by Text ##
g = call_loop_concat.groupby(['VOICE_ID','SPEAKER'], as_index=False)['TEXT'].apply(lambda TEXT: "" .join(TEXT)).to_frame().reset_index()
g.columns.values[2] = "TEXT"

## Merge main_data and g table for analysis ##
full_data = pd.merge(main_data,g,on='VOICE_ID')

## Save data in csv file ## 
full_data.to_csv('misumi_cs.csv', encoding = 'utf-8')




