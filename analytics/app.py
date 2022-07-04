from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from flask import jsonify
import json
import csv
import os

app = Flask(__name__)

@app.route('/')
def root():
  return  render_template('status.html')

@app.route('/api/get')
def get():
   data = '['
   
   with open('api.json', 'r') as json_file:
      for line in json_file:
         data += line
   return jsonify({'data': json.loads(data[0:-1] + ']')})
 
   
@app.route('/api/post', methods = ['POST'])
def post():
   response = Response()
   response.headers['Access-control-Allow-Origin'] = '*' 
    
   stats = {
       'Agent' : request.headers.get('User-Agent'),
       'Date' : request.form.get('Date'),
       'Url' : request.form.get('Url')
       
    } 
    
   if request.headers.getlist('X-Forwarded-For'):
      stats['Ip'] = request.headers.getlist('X-Forwarded-For')[0]
   else:
        stats['Ip'] = request.remote_addr
        
   if request.headers.get('Origin'):
      stats['Origin'] = request.headers.get('Origin')
   else:
      stats['Origin'] = 'N/A'   
           
   try:
       os.remove('abx.csv')
   except OSError:
       pass 
   
        
   with open('api.json', 'a') as json_file:
       json_file.write(json.dumps(stats, indent = 2) + ',' + '\n')
   
   return response    
  
 
if __name__ == '__main__':
   app.run(debug = True, threaded = True)  
