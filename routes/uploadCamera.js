var express = require('express');
var router = express.Router();
var multer  =   require('multer');
var child_process = require('child_process')
var shortid = require('shortid');
var util = require("util");


var storage =   multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, './user/camera/'+ req.body.mediaId);
    },
    filename: function (req, file, callback) {
        callback(null, file.fieldname + '-' + shortid.generate());
    }
});


var upload = multer({ storage : storage }).array('cameraImgs',100);

router.post('/upload', function(req,res){
    upload(req, res, function(err) {
        console.log(req.body);
        console.log(req.files);
        if(err) {
            return res.end("Error uploading file.");
        }

        var spawn = child_process.spawn;

        var process = spawn('python',["python/acceptCameraImgs.py", req.body.mediaId]);
        process.stdout.on('data',function(chunk){
           var textChunk = chunk.toString('utf8');// buffer to string
           util.log(textChunk);
        });

        process.stderr.on('data', (data) => {
           console.log(`stderr: ${data}`);
        });

        process.on('close', (code) => {
           if(code == 0) {
               res.end("File is uploaded");
           } else {
               return res.status( 403 ).send( "The image provided was not able to be processed. ")
           }
        });
    });
});

module.exports = router
