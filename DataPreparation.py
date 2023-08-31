import pandas as pd
import sys
import re

data = pd.read_csv(sys.argv[0], sep='\t', index_col=False)
data.dropna(inplace=True)
print(sys.argv[0], 'shape: ' , data.shape)
codes = pd.read_csv(sys.argv[1], sep=',', index_col=False)
print(sys.argv[1], 'shape: ' , codes.shape)
inner_join = pd.merge(data, codes, on =['account_number'], how ='inner')
inner_join.encounter_id = inner_join.encounter_id.astype(int)
inner_join.account_number = inner_join.account_number.astype(int)
ml_df = inner_join.copy()
ml_df['ADDENDUM'] = 0
ml_df['ADMIT'] = 0
ml_df.MDM_SENTS = ml_df.MDM_SENTS.apply(str.lower)

for i, r in ml_df.iterrows():
    if 'addendum' in str(r['MDM_SENTS']):
        ml_df.loc[i, 'ADDENDUM'] = 1

for i, r in ml_df.iterrows():
    if 'Admitted' in str(r['ADMISSION_STATUS']):
        ml_df.loc[i, 'ADMIT'] = 1
        
for i,r in ml_df.iterrows():
    ml_df.loc[i,'clean_eandm_suggested'] = ','.join([str(elem) for elem in re.findall(r"\b\d{5}\b", str(r['eandm_suggested']))])
    ml_df.loc[i,'clean_eandm_final'] = ','.join([str(elem) for elem in re.findall(r"\b\d{5}\b", str(r['eandm_final']))])
    
ml_df.clean_eandm_suggested = ml_df.clean_eandm_suggested.astype('str')
ml_df.clean_eandm_final = ml_df.clean_eandm_final.astype('str')
ml_df['TIME_CASES'] = 0

for i, r in ml_df.iterrows():
    if '99291' in r['clean_eandm_suggested'] or '99291' in r['clean_eandm_final']:
        ml_df.loc[i, 'TIME_CASES'] = 1
        
ml_df_final = ml_df[(ml_df.TIME_CASES == 0) & (ml_df.ADDENDUM == 0) & (ml_df.ADMIT == 0)].reset_index()
ml_df_final.drop(['index'], inplace=True, axis=1)
ml_df_final.to_excel(sys.argv[0], index=False)