var express =   require("express");
var bodyParser =    require("body-parser");
var app =   express();
var uploadCamera = require('./routes/uploadCamera.js');
var calibrationImg = require('./routes/calibrationImg.js');
var warpMedia = require('./routes/warpMedia.js');

app.use( bodyParser.json() );
app.use( express.static( __dirname + '/semantic' ) );
app.use( express.static( __dirname + '/views' ) );
app.use( express.static( __dirname + '/user' ) );

app.use('/uploadCamera', uploadCamera);
app.use('/calibrationImg', calibrationImg);
app.use('/warpMedia', warpMedia)


app.get('/',function(req,res){
    res.sendFile(__dirname + "/views/index.html");
});



app.listen(3000,function(){
    console.log("Working on port 3000");
});
