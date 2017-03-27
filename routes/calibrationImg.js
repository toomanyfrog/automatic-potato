var express = require('express');
var router = express.Router();
var multer  =   require('multer');
var child_process = require('child_process')
var util = require("util");


var storage =   multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, './user/uploads');
    },
    filename: function (req, file, callback) {
        callback(null, file.fieldname + '-' + Date.now());
    }
});

var upload = multer({ storage : storage }).single('media');

router.post('/upload', function(req,res){
    upload(req, res, function(err) {
        console.log(req.body);
        console.log(req.file);
        if(err) {
            console.error(err);
            return res.end("Error uploading file.");
        }
        var spawn = child_process.spawn;
        var dir = "./user/generated/" + req.file.filename;

        var process = spawn('python',["python/generateImgs.py", req.body.rows, req.body.cols, req.file.filename]);
        process.stdout.on('data',function(chunk){
           var textChunk = chunk.toString('utf8');// buffer to string
           util.log(textChunk);
        });

        process.stderr.on('data', (data) => {
           console.log(`stderr: ${data}`);
        });

        process.on('close', (code) => {
           if(code == 0) {
               res.send( { filename: req.file.filename,
                           numDots: req.body.rows * req.body.cols });
               //sendFile( "processed/" + req.file.filename + ".jpg", { root: __dirname } );
           } else {
               return res.status( 200 ).send( "The image provided was not able to be processed. ")
           }
        });

    });
});

module.exports = router;
