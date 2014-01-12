// Webscraper of http://scorecard.assetsandopportunity.org/2013/measure/net-worth?state=il

var page = require('webpage').create();

var wealth_array = page.open('http://scorecard.assetsandopportunity.org/2013/measure/net-worth?state=il', function(status) {
  if (status !== 'success') {
    console.log('Unable to access network');
  } else {
    var ua = page.evaluate(function() {
      return document.getElementById('sco-measures').textContent;
    });
    ua = ua.split(/\s+/).slice(8,-1);
    var j = 0
    while (j < ua.length) {
    	if (ua[j] === "*") {
    		ua.splice(j, 1);
    	} else {
    		j++
    	}
    }

   console.log('done')
   console.log(ua)


  }

  phantom.exit();

});


