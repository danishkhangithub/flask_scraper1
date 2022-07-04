import scrapy 
from scrapy.crawler import CrawlerProcess
import json
import re
import os


class Wellness(scrapy.Spider):
   
   name = 'wellness'
   allowed_domains = ['wellness.com']
   
   base_url = 'https://www.wellness.com/find/acupuncturist/alphabetical-index/a' 
   
   try:
      os.remove('wellness.jsonl')
   except OSError:
        pass
  
   def start_requests(self):
     
     settings = ''
     
     with open('settings.json', 'r') as f:
       for line in f.read():
          settings += line
       
       settings = json.loads(settings)
    
     yield scrapy.Request(url = 'https://www.wellness.com/find/%s' %settings['category'], callback = self.state)
     
   def state(self, response):
    states =  response.css('div.find-item-container h2.h3-style::text').getall()
    states = [state[-3:-1] for state in states]
    for state in states:
         state = state.lower()
         state = 'https://www.wellness.com/find/acupuncturist/'+str(state)
         
         yield response.follow(url = state, callback = self.city)      
         break
         
   def city(self, response):
      for a in response.css('li.categories-li a'):
          yield response.follow(a, callback = self.profile_link)
          break
   def profile_link(self, response):
     for a in response.css('h2 a'):
        yield response.follow(a, callback = self.profile)
        
        
   def profile(self, response):
       services = response.xpath('//span[contains(text(),"Services")]')
       education = response.xpath('//span[contains(text(),"Education")]')
       try:
        training = response.xpath('.//span[contains(text(),"Training")]')[1]
       except:
        training = 'N/A'
       
       items = {}
       
       items['First_and_Last_Name'] = response.css('h1::text').get()
       items['About'] = response.css('span.listing-about::text').get()
       items['Services'] = services.xpath('following-sibling::span[1]/text()').extract()
       items['Primary_Specialty'] = response.css('h2.normal::text').extract()
       items['Practice'] = response.css('span.listing-h2::text').get()
       items['Education'] = education.xpath('following-sibling::span/text()').extract()
       try:
          items['Training'] = training.xpath('following-sibling::span[1]/text()').extract()
       except:
          items['Training'] = 'N/A'
       
       review_link = response.css('.after-poll-reviews  a::attr(href)').get()
       if review_link is not None:
         yield scrapy.Request(response.urljoin(review_link), callback = self.parse_reviews,meta = {'item': items})
       
       else:
         directions_link = response.css('#directions_tab a::attr(href)').get()
         yield scrapy.Request(response.urljoin(directions_link), callback=self.parse_directions, meta={'item': items})   
         
       
   def parse_reviews(self, response):
      items = response.meta['item']  
      items['Customer Feedback'] = response.css('.item-rating-container a::text').get() 
       
      directions_link = response.css('#directions_tab a::attr(href)').get()
      yield scrapy.Request(response.urljoin(directions_link), callback = self.parse_directions, meta = {'item':items})

   def parse_directions(self, response):
       items = response.meta['item']
       
       address = response.css('.item-separator+ span::text').get()
       
       items['Phone'] = response.css('.tel::text').get()
       items['Address'] = address

       with open('wellness.jsonl', 'a') as f:
         f.write(json.dumps(items, indent = 2)+ '\n')
            
               
#main driver      
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Wellness)
    process.start()
      
   
