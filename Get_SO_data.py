# get StackOverflow data
from stackapi import StackAPI
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

#set Stack Overflow parameters
SITE = StackAPI('stackoverflow')
SITE.page_size= 100
SITE.max_pages = 100
#SITE.key = 'AQv9CZcew3UHzI*9JoZ3gA(('
post = SITE.fetch('questions',fromdate=datetime(2019,1,1), todate=datetime(2019,11,15))

#getting data from Stack Overflow
data = post['items']

post_dict = { 'owner': [],'score':[],'last_edit_date':[],'last_activity_date':[],'creation_date':[],'q_id':[],'q_link':[], 'q_text':[]}

counter = 0 # counter for calls to the site for scraping
q_count = 1

#write data to pandas
for ele in data:
    
    print('counter:',q_count,'collecting data for', ele['question_id'])
    
    #get the user info
    if 'owner' in ele:
        if 'link' in ele['owner'].keys():
            post_dict['owner'].append(ele['owner']['link'])
        else:
            post_dict['owner'].append('no_value')
      
    else:
        post_dict['owner'].append('no_value')
        
        
    #get the score info
    if 'score' in ele:
        post_dict['score'].append(ele['score'])
    else:
        post_dict['score'].append('no_value')
        
    #get the date of last edit
    if 'last_edit_date' in ele:
        ts = int(ele['last_edit_date'])
        edit_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        post_dict['last_edit_date'].append(str(edit_date))
    else:
        post_dict['last_edit_date'].append('no_value')
        
    #get the last activity date
    if 'last_activity_date' in ele:
        ts1 = int(ele['last_activity_date'])
        activity_date = datetime.utcfromtimestamp(ts1).strftime('%Y-%m-%d %H:%M:%S')
        post_dict['last_activity_date'].append(str(activity_date))
    else:
        post_dict['last_edit_date'].append('no_value')
    
    #get the last creation date 
    if 'creation_date' in ele:
        ts2 = int(ele['creation_date'])
        creation_date = datetime.utcfromtimestamp(ts2).strftime('%Y-%m-%d %H:%M:%S')
        post_dict['creation_date'].append(str(creation_date))
    else:
        post_dict['creation_date'].append('no_value')
    
    #get the question id
    if 'question_id' in ele:
        post_dict['q_id'].append(ele['question_id'])
    else:
        post_dict['q_id'].append('no_value')
    
    #get the post link
    if 'link' in ele:
        post_dict['q_link'].append(ele['link'])
        
        # scrape out the post text
        url = ele['link']
        
        try:
            page = requests.get(url)
            counter+=1 # update website hit rate
        
            # make it sleep every 500 calls
            if counter == 500: 
                print('off to sleep ....')
                time.sleep(450)
                print('resuming after sleep')
            
        
            #print(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                question = soup.find('div', class_='post-text')
                #print(question)
                q_data = question.get_text()
                if q_data != None:
                    q_data_fin = ''
                    data_points = q_data.split('\n')
                    if len(data_points) > 0:
                        for p in data_points:
                            q_data_fin+=p
                        post_dict['q_text'].append(q_data_fin)
                    else:
                        post_dict['q_text'].append('check')
                else:
                    post_dict['q_text'].append('check')
                
                
                
            elif page.status_code == 429:
                post_dict['q_text'].append('get_later')
                
        except:
            post_dict['q_text'].append('get_later')
            
           
    else:
        post_dict['q_link'].append('no_value')
        post_dict['q_text'].append('no_value')
        
    q_count+=1
        

for e in post_dict.keys():
    print(len(post_dict[e]))
    
final_data = pd.DataFrame(post_dict)

final_data.to_csv("Post_data_new_dataset.csv")
    





