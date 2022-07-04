###############################
#     Csv to Ecommerce
#          by 
#
#       Danish khan
#
#
###############################
#packages
from flask import *
import csv

# create app instance
app = Flask(__name__)

# create http route
@app.route('/')
def root():
   with open('lulu.csv', 'r') as f:
       data = [dict(item) for item in csv.DictReader(f)]
       try:
         page = int(request.args.get('page'))
       except:
         page = 0
       
       # display item per page 
       items_per_page = 5
       
       # starting index 
       index_from = 0
       
       # calculate starting index
       for index in range(page-1):
           index_from += items_per_page
       index_to = index_from + items_per_page
       
       print('page:', page) 
       print('per_page:', items_per_page ) 
       print('from:', index_from ) 
       print('to:', index_to)             
       
       total_pages = range(int(len(data)/ items_per_page) + 1)
       
       return render_template_string('''
            <html>
               <head>
                  <title>Rice & Grocery</title>
                  <link rel="stylesheet" href
                  = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
               </head>
               
               <body>
                 <div class = "card">
                   <div class = "card-header">
                     <h2 class = "text-center">Rice and Grocery</h2>
                   </div>  
                 </div>                 
                 
                 <div class = "container mt-4">
                   {% for item in data %}
                     <div class = "card mt-4">
                       <div class = "card-body">
                         <div class = "row">
                           <div class = "col-10">
                              <h4>{{item.title}}</h4>
                              <p><strong>{{item.price}}</strong></p>
                              <span>{{item.Brand}}</span>
                              <span>{{item.Content}}</span>
                              <span>{{item.Type}}</span>                              
                           </div>
                           <div class = "col-2">
                             <img src="{{item.thumbnail_url}}">
                           </div>
                         </div>
                       </div>
                     </div>
                   {% endfor %}
                   <div class = "text-center">
                     {% for page in total_pages %} 
                       <a href = "{{str(request.url).split('?')[0] + '?page=' + str(page + 1)}}" class = "btn btn-outline-primary mt-4 mb-2">{{page + 1}}</a> 
                     {% endfor %}
                   </div>
                 </div>
                 <div class = "card">
                   <div class = "card-footer mt-4 mb-4">
                     <p class = "text-center">
                       Created by Danish khan
                       <br>
                       <strong>
                          danishkhankd237@gmail.com
                       </strong>
                     </p>
                   </div>
                 </div>
               </body>
            
            </html>
       
       ''', data = data[index_from:index_to], total_pages = total_pages, str= str)
       
 
if __name__ == '__main__':
   app.run(debug = True, threaded = True)       

