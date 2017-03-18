var express   =   require( 'express' );
var multer    =   require( 'multer' );
var bodyParser = require('body-parser');
var sizeOf    =   require( 'image-size' );
var exphbs    =   require( 'express-handlebars' );
var child_process = require("child_process")
var fs = require('fs');
require( 'string.prototype.startswith' );
var util = require("util");



var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
      console.log(file);
    cb(null, file.fieldname + '-' + Date.now())
  }
});
var upload = multer( { storage: storage  } ); //dest: 'uploads/' } );

var app = express();

app.use( express.static( __dirname + '/bower_components' ) );
app.use('/processed', express.static('processed'))
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
//app.use(express.static('/assets/styles '));


app.engine( '.hbs', exphbs( { extname: '.hbs' } ) );
app.set('view engine', '.hbs');

app.get( '/', function( req, res, next ){
    return res.render( 'index' );
});

app.post( '/upload', upload.single( 'file' ), function( req, res, next ) {

    if ( !req.file.mimetype.startsWith( 'image/' ) ) {
        return res.status( 422 ).json( {
            error : 'The uploaded file must be an image'
        } );
    }

    var dimensions = sizeOf( req.file.path );
    if ( ( dimensions.width < 320 ) || ( dimensions.height < 240 ) ) {
        return res.status( 422 ).json( {
            error : 'The image must be at least 320 x 240px'
        } );
    }
    var spawn = child_process.spawn;

    var process = spawn('python',["python/matcher.py", req.file.path, req.file.filename]);
    process.stdout.on('data',function(chunk){
        var textChunk = chunk.toString('utf8');// buffer to string
        util.log(textChunk);
    });

    process.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    process.on('close', (code) => {
        if(code == 0) {
            return res.status( 200 ).send("processed/" + req.file.filename + ".jpg");
            //sendFile( "processed/" + req.file.filename + ".jpg", { root: __dirname } );
        } else {
            return res.status( 200 ).send( "The image provided was not able to be processed. ")
        }
    });

});

app.listen( 8080, function() {
    console.log( 'Express server listening on port 8080' );
});
