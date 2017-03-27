var express = require('express');
var router = express.Router();
var multer  =   require('multer');

var storage =   multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, './user/camera');
    },
    filename: function (req, file, callback) {
        callback(null, file.fieldname + '-' + Date.now());
    }
});


var upload = multer({ storage : storage }).array('userPhoto',2);

router.post('/upload', function(req,res){
    upload(req, res, function(err) {
        console.log(req.body);
        console.log(req.files);
        if(err) {
            return res.end("Error uploading file.");
        }
        res.end("File is uploaded");
    });
});

module.exports = router
