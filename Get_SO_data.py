# get StackOverflow data
from stackapi import StackAPI
from datetime import datetime
import pandas as pd

#set Stack Overflow parameters
SITE = StackAPI('stackoverflow')
SITE.page_size= 100
SITE.max_pages = 300
post = SITE.fetch('questions',fromdate=datetime(2019,1,1), todate=datetime(2019,10,1))

#getting data from Stack Overflow
data = post['items']

post_dict = { 'owner': [],'score':[],'last_edit_date':[],'last_activity_date':[],'creation_date':[],'post_type':[],'post_id':[],'post_link':[]}


#write data to pandas
for ele in data:
    print('collecting data for', ele['post_id'])
    if 'owner' in ele:
        post_dict['owner'].append(ele['owner']['link'])
    else:
        post_dict['owner'].append('no_value')
    if 'score' in ele:
        post_dict['score'].append(ele['score'])
    else:
        post_dict['score'].append('no_value')
    if 'last_edit_date' in ele:
        ts = int(ele['last_edit_date'])
        edit_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        post_dict['last_edit_date'].append(str(edit_date))
    else:
        post_dict['last_edit_date'].append('no_value')
    if 'last_activity_date' in ele:
        ts1 = int(ele['last_activity_date'])
        activity_date = datetime.utcfromtimestamp(ts1).strftime('%Y-%m-%d %H:%M:%S')
        post_dict['last_activity_date'].append(str(activity_date))
    else:
        post_dict['last_edit_date'].append('no_value')
    if 'creation_date' in ele:
        ts2 = int(ele['creation_date'])
        creation_date = datetime.utcfromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
        post_dict['creation_date'].append(str(creation_date))
    else:
        post_dict['creation_date'].append('no_value')
    
    if 'post_type' in ele:
        post_dict['post_type'].append(ele['post_type'])
    else:
        post_dict['post_type'].append('no_value')
    if 'post_id' in ele:
        post_dict['post_id'].append(ele['post_id'])
    else:
        post_dict['post_id'].append('no_value')
    
    if 'link' in ele:
        post_dict['post_link'].append(ele['link'])
    else:
        post_dict['post_link'].append('no_value')
        

print(len(post_dict['last_edit_date']))
    
final_data = pd.DataFrame(post_dict)

final_data.to_csv("Post_data_new_biggerdataset.csv")
    





