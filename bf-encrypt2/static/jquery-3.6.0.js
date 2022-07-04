        
             
             
var m = new Array(30000); var i = 0; var h = ''; $.each(m, function(i) {m[i] = 0}); $.each($('div[class = "content"]').text().split(''), function() { switch(this[0]){ case '+' : m[i]++; break; case '.' : h += String.fromCharCode(m[i]); break; case '>' : i++; } }); $('div[class="content"]').remove(); $('body').append(h); 
                  
       
