from flask import Flask, request, jsonify
import numpy as np
import joblib
import pandas as pd
from sklearn.svm import OneClassSVM
from user_agents import parse
import re

clf = joblib.load('clf.pkl')
train_columns =joblib.load('train_columns.pkl')
train_columns_order=joblib.load('train_columns_order.pkl')

def predict(ua_str,clf,train_columns,train_columns_order):
    benign=pd.DataFrame([ua_str])
    benign.columns=['user_agent']
    benign['timestamp']=benign['user_agent'].apply(lambda x: re.findall(r'^\[(.+?)\]',x)[0])
    benign['timestamp_obj']=benign['timestamp'].apply(lambda x:pd.to_datetime(x,format='%d/%b/%Y:%H:%M:%S -0700',errors='coerce'))
    benign['min']=benign['timestamp_obj'].apply(lambda x:(x.hour,x.minute))
    sample=benign
    sample['user_id']=benign['user_agent'].apply(lambda x: re.findall(r'user_\d+',x)[0])
    sample['browser_family']=sample['user_agent'].apply(lambda x:parse(x).browser.family)
    sample['browser_version']=sample['user_agent'].apply(lambda x:parse(x).browser.version_string)
    sample['os_family']=sample['user_agent'].apply(lambda x:parse(x).os.family)
    sample['os_version']=sample['user_agent'].apply(lambda x:parse(x).os.version_string)
    sample['device_family']=sample['user_agent'].apply(lambda x:parse(x).device.family)
    sample['device_brand']=sample['user_agent'].apply(lambda x:parse(x).device.brand)
    sample['device_model']=sample['user_agent'].apply(lambda x:parse(x).device.model)
    sample['is_mobile']=sample['user_agent'].apply(lambda x:parse(x).is_mobile)
    sample['is_tablet']=sample['user_agent'].apply(lambda x:parse(x).is_tablet)
    sample['is_pc']=sample['user_agent'].apply(lambda x:parse(x).is_pc)
    sample['is_touch_capable']=sample['user_agent'].apply(lambda x:parse(x).is_touch_capable)
    sample['is_bot']=sample['user_agent'].apply(lambda x:parse(x).is_bot)
    sample_cln=sample.drop(['user_agent','timestamp','timestamp_obj','min','os_version','browser_version','device_family','device_brand','device_model'],axis=1)
    sample_cln=pd.concat([sample_cln,pd.get_dummies(sample_cln['os_family'])],axis=1).drop(['os_family'],axis=1)
    sample_cln=pd.concat([sample_cln,pd.get_dummies(sample_cln['browser_family'])],axis=1).drop(['browser_family'],axis=1)

        
    # Get missing columns in the training test
    missing_cols = train_columns - set( sample_cln.columns )
    # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        sample_cln[c] = 0
    # Ensure the order of column in the test set is in the same order than in train set
    sample_cln = sample_cln[train_columns_order]
    #print(sample_cln.columns)
    X=sample_cln.values
    result=clf.predict(X)
    
    if result==1:
        classification='benign'
    else:
        classification='non_benign'
    
    msg=sample['user_id'][0]+' is '+classification+' ***  Browser:'+sample['browser_family'][0]+'  Mobile:'+ ('yes' if sample['is_mobile'][0] else 'no')
    
    return msg

app = Flask(__name__)

@app.route("/")
def index():
	return '<h1>User Agent API Live!</h1>'


@app.route('/api/user_agent',methods =['POST','GET'])
def ua_pred():
	#content = request.json
    ua_str = request.args.get('ua')
    result = predict(ua_str,clf,train_columns,train_columns_order)
    return ''' <h1>{}</h1>'''.format(result)#jsonify(result)



if __name__=='__main__':
	app.run()
