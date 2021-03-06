# coding: utf-8

## Loading Relevant libraries
import pandas as pd

## Getting full data in
renaloc = pd.read_csv('../../data/processed/renaloc_full.csv' , encoding = "ISO-8859-1" )

## Keeping only data with geolocation
geolocalized_data = renaloc[pd.isnull(renaloc.longitude) == False]
geolocalized_data.to_csv('../../data/processed/renaloc_geolocalized.csv' , index = False)

## Other output for localities only
locality_data = renaloc[renaloc.level == 'Localite']
locality_data.to_csv('../../data/processed/renaloc_localities.csv' , index = False)

del locality_data

## Taking out duplicate voters (probably from pb in extraction of voters data, may be should be done earlier)
voters_data = pd.read_csv('../../data/processed/voters_list.csv' , encoding = "ISO-8859-1")

## For efficiency, splitting voters data, process separately part with doublon voters
n_ids = voters_data['unique_ID'].value_counts()
doublons = n_ids[n_ids > 1]

doub_data = voters_data[voters_data.unique_ID.isin(list(doublons.keys()))]
unique_data = voters_data[~(voters_data.unique_ID.isin(list(doublons.keys())))]

def keep_unique_voters(data):
    return data.iloc[0]

d = doub_data.groupby('unique_ID').apply(keep_unique_voters)
dedoubled = d.reset_index(drop = True)

final = unique_data.append(dedoubled)
final = final.reset_index(drop = True)

final.to_csv('../../data/processed/voters_list.csv' , index = False)

del voters_data
del unique_data

## Export N of voters by bureau
def get_bureaux_size(data):
    name = data.bureau.iloc[0]
    pop = len(data)
    commune_ID = data.commune_ID.iloc[0]
    bureau_ID = data.bureau_ID.iloc[0]
    out = pd.DataFrame([{'commune_ID':commune_ID , 'bureau':name , 'N_voters':pop}])
    return out

voting_centers_size = final.groupby('bureau_ID').apply(get_bureaux_size)
voting_centers_size = voting_centers_size.reset_index()
voting_centers_size = voting_centers_size[['bureau_ID' , 'commune_ID' , 'bureau' , 'N_voters']]

voting_centers_size.to_csv('../../data/processed/voting_bureaux_size.csv')
