let newsTitle = ''




document.querySelector('#title').addEventListener('focusout', function (e) {
     newsTitle = e.target.value
     console.log(newsTitle)

     var pg = require('pg')
     const conString = "postgres://yaquake:uVbiho60@localhost:5432/mcsite"
     const client = new pg.Client(conString)
     client.connect()
     const query = client.query("SELECT * FROM main_news WHERE name=newsTitle")
     if (query) {
          alert('Hello')
     }
})