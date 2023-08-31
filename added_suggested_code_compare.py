
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import re

user = 'read_only'
pwd = quote_plus('P@ssw0rd@123')
host = '10.10.211.59:3306'
db_name = 'CAPC_ACCURACY_REPORT'

db_connection_str = 'mysql+pymysql://{}:{}@{}/{}'.format(user,pwd,host,db_name)
db_connection = create_engine(db_connection_str)

query ='''SELECT * FROM CAPC_ACCURACY_REPORT.overall_data where month in ('2023-06') and client_code='CHS';'''

df=[]
df.append(pd.read_sql(query, con=db_connection))

def clean(x):

    x=str(x)
    new_code=''
    if re.match('.*9921[1-5].*',x) and re.match('.*9920[1-5].*',x):
        codes=x.split(',')
        for code in codes:
            if re.match('.*9921[1-5].*', code):
                new_code=code.strip()   
    
    
    if re.match('.*992[0-9]{2}.*',x) and re.match('.*994[0-9]{2}.*',x):
        codes=x.split(',')
        for code in codes:
            if re.match('.*992[0-9]{2}.*', code):
                new_code=code.strip()   
               
    if new_code!='':
        codes=re.findall('\d{5}',new_code)
    else:
        codes=re.findall('\d{5}',x)
    codes.sort()
    
    if codes!=[]:
        return codes[-1]
    else:
        return '[]'
    
for df_new in df:
    df_new['new_sugg'] = df_new.eandm_suggested.apply(clean)
    df_new['new_final'] = df_new.eandm_final.apply(clean)

def get_category_1(x):
    sugg = str(x.new_sugg)
    final = str(x.new_final)
    
    
    # a
    if sugg == "[]" and re.match('.*(992[018]{1}5).*',final):
        return "category_1_a"

    # b
    elif sugg == '[]' and re.match('.*(9929[12]).*',final):
        return "category_1_b"

    # c
    elif sugg == "[]" and re.match('.*(9944[1-3]).*',final):
        return "category_1_c"

    # d
    elif sugg == "[]" and re.match('.*(993[8-9][1-7]).*',final):
        return "category_1_d"

    # e
    elif sugg == "[]" and re.match('\d.*',final):
        return "category_1_e"
        
    return "null"

for df_new in df:
    df_new['category1'] = df_new.apply(get_category_1, axis=1)

def get_category_2a(x):
    sugg = x.new_sugg
    final = str(x.new_final)
    
    # i
    if re.match('.*9928[1-5].*',sugg) and re.match('.*9929[12].*',final):
        return "category_2a_i"

    # ii
    elif re.match('.*9929[12].*',sugg) and re.match('.*9928[1-5].*',final):
        return "category_2a_ii"

    # iii
    elif re.match('.*9944[1-3].*',sugg) and re.match('.*992[01][2-5].*',final):
        return "category_2a_iii"

    # iv
    elif re.match('.*992[01][2-5].*',sugg) and re.match('.*9944[1-3].*',final):
        return "category_2a_iv"

    # v
    elif re.match('.*992[01][2-5].*',sugg) and re.match('.*993[89][1-7].*',final):
        return "category_2a_v"

    # vi
    elif re.match('.*993[89][1-7].*',sugg) and re.match('.*992[01][2-5].*',final):
        return "category_2a_vi"
    
    # vii
    elif re.match('.*9928[1-5].*',sugg) and re.match('.*992[23][2-6].*',final):
        return "category_2a_vii"
    
    # viii
    elif re.match('.*992[23][2-6].*',sugg) and re.match('.*9928[1-5].*',final):
        return "category_2a_viii"

    return "null"

for df_new in df:
    df_new['category2a'] = df_new.apply(get_category_2a, axis=1)
    

def get_category_2b(x):
    sugg = x.new_sugg
    final = str(x.new_final)
    
    # i
    if re.match('.*9920[1-5].*',sugg) and re.match('.*9921[1-5].*',final):
        return "category_2b_i"
    # ii
    elif re.match('.*9921[1-5].*',sugg) and re.match('.*9920[1-5].*',final):
        return "category_2b_ii"

    # iii
    elif re.match('.*9938[1-7].*',sugg) and re.match('.*9939[1-7].*',final):
        return "category_2b_iii"

    # iv
    elif re.match('.*9939[1-7].*',sugg) and re.match('.*9938[1-7].*',final):
        return "category_2b_iv"
    
    # v
    elif re.match('.*9922[1-3].*',sugg) and re.match('.*9923[1-3].*',final):
        return "category_2b_v"
    
    # vi
    elif re.match('.*9923[1-3].*',sugg) and re.match('.*9922[1-3].*',final):
        return "category_2b_vi"

    return "null"


for df_new in df:
    df_new['category2b'] = df_new.apply(get_category_2b, axis=1)

def get_category_2c(x):
    sugg = x.new_sugg
    final = str(x.new_final)

    # i
    if re.match('.*9928[1-4].*',sugg) and re.match('.*99285.*',final):
        return "category_2c_i"

    # ii
    elif re.match('.*99285.*',sugg) and re.match('.*9928[1-4].*',final):
        return "category_2c_ii"

    # iii
    elif re.match('.*992[01][2-3].*',sugg) and re.match('.*992[01]4.*',final):
        return "category_2c_iii"

    # iv
    elif re.match('.*992[01]5.*',sugg) and re.match('.*992[01][1-4].*',final):
        return "category_2c_iv"
    
    # v
    elif (sugg=='99291' and final=='99292') or (sugg=='99292' and final=='99291'): 
        return "category_2c_v"

    return "null"

for df_new in df:
    df_new['category2c'] = df_new.apply(get_category_2c, axis=1)

def get_match(sug, fin):

    if sug==fin:
        return True
    return False


def get_not_accepted(x):
    sugg = x.new_sugg
    final = str(x.new_final)

    # a they didn't accept any code
    if re.match('\d.*',sugg) and final=='[]':
        return "category_3a"

    # b the exact match code
    elif get_match(sugg, final):
        return "category_3b"

    return "other"

for df_new in df:
    df_new['category3'] = df_new.apply(get_not_accepted, axis=1)


def get_final_category(x):
    cat1=x.category1
    cat2a=x.category2a
    cat2b=x.category2b
    cat2c=x.category2c
    cat3=x.category3
    
    if cat1!="null":
        return cat1
        
    if cat2a!="null":
        return cat2a
    
    if cat2b!="null":
        return cat2b
    
    if cat2c!="null":
        return cat2c
    
    if cat3!="null":
        return cat3
        
    return "null"


for df_new in df:
    df_new['final_category'] = df_new.apply(get_final_category, axis=1)

# category 1: When we did not suggest any code:
# 	a) How many level 5 codes
# 	b) how many critical care codes: 91, 92
# 	c) How many telephone codes: 441 - 443
# 	d) preventive 381-387 & 91-97
# 	e) How many other codes

# Category 2: We suggested wrong code:
# 	a) how many times we missed the place of care
# 		i) We suggested 81-85, they added 91, 92
# 		ii) We suggested 91, 92, they added 81-85
# 		iii) We suggested 441 - 443, they added 212-215
# 		iv) We suggested 212-215, they added 441, 443
# 		v) we suggested 212-215 and they added 381-387 & 391-397
# 		vi) we suggested 381-387 & 391-397 and they added 212-215
# 		vii) we suggested 81-85, they added 99221-99236
# 		vii) we suggested 99221-99236, they added 81-85
# 	b) How many visit types we mismatched
# 		i) We suggested NP 201 - 205, they added EP 212 - 215
# 		ii) We suggested EP 212 - 215, they added NP 201 - 205
# 		iii) we suggested NP 381-387 and they added 391-397
# 		iv) we suggested NP 391-397 and they added 381-387
# 		v) We suggested EP 221 - 223, they added NP 231 - 233
# 		vi) We suggested EP 231 - 233, they added NP 221 - 223
# 	c) How many level 5 mismatch in same place of care
# 		i) We suggested 81 - 84, they added 85
# 		ii) We suggested 85, they added 81 - 84
# 		iii) We suggested 212-214 or 201-204, they added 205 or 215
# 		iv) We suggested 205 or 215, they added 212-214 or 201-204
# 		v) miss-match with 91 and 92

# Category 3: final result
# 	a) they didn't accept any code
# 	b) they accepted our code

# code range of facilities

def get_code_range(x):
    final = str(x.new_final)
                
    if final=='nan' or final=='[]':
        return 'other'

    code=int(final)
    
    if code>=99201 and code<=99205:
        return '99202-99205'
    
    if code>=99211 and code<=99215:
        return '99212-99215'
    
    if code>=99281 and code<=99285:
        return '99281-99285'
    
    if code>=99291 and code<=99292:
        return '99291-99292'
    
    if code>=99221 and code<=99223:
        return '99221-99223'
    
    if code>=99231 and code<=99233:
        return '99231-99233'
    
    if code>=99234 and code<=99236:
        return '99234-99236'
    
    if code>=99238 and code<=99239:
        return '99238-99239'
    
    if code>=99381 and code<=99387:
        return '99381-99387'
    
    if code>=99391 and code<=99397:
        return '99224-99226'
    
    if code>=99251 and code<=99255:
        return '99251-99255'
    
    if code>=99218 and code<=99220:
        return '99218-99220'
    
    if code>=99224 and code<=99226:
        return '99224-99226'
    
    if code==99217:
        return '99217'
    
    return 'other'

for df_new in df:
    df_new['code_range']=df_new.apply(get_code_range, axis=1)


# find code ranges per facility

code_ranges=[]

for df_new in df:
    code_ranges.append(df_new.code_range.unique())

def check_row(x):
    if x.account_number==7763806:
        print(x)

for df_new in df:
    df_new.apply(check_row, axis=1)

df_new=pd.concat(df)

df_new.final_category.value_counts()
df_new.loc[:, ~df_new.columns.isin(['new_sugg', 'new_final'])].to_excel('new_py_output1.xlsx', index=False)
