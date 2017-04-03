function imgToCanvas(e, ctx) {
    var ctx = document.getElementById('imageForRect').getContext('2d');
    var ctx2 = document.getElementById('drawRect').getContext('2d');

    var reader  = new FileReader();
    var file = e.target.files[0];
    // load to image to get it's width/height
    var img = new Image();
    img.onload = function() {
        // scale canvas to image
        ctx.canvas.width = img.width;
        ctx.canvas.height = img.height;
        // draw image
        ctx.drawImage(img, 0, 0, ctx.canvas.width, ctx.canvas.height);

        ctx2.canvas.width = img.width;
        ctx2.canvas.height = img.height;
        // draw image
        ctx2.drawImage(img, 0, 0, ctx.canvas.width, ctx.canvas.height);
    }
    // this is to setup loading the image
    reader.onloadend = function () {
        img.src = reader.result;
    }
    // this is to read the file
   	reader.readAsDataURL(file);
}

$(document).ready(function() {
    var input = document.getElementById('cameraImgs');
    input.addEventListener('change', imgToCanvas, false);

    var canvas, context, startX, endX, startY, endY;
    var mouseIsDown = 0;

    function init() {
        canvas = document.getElementById("drawRect");
        context = canvas.getContext("2d");

        canvas.addEventListener("mousedown", mouseDown, false);
        canvas.addEventListener("mousemove", mouseXY, false);
        canvas.addEventListener("mouseup", mouseUp, false);
    }

    function mouseUp(eve) {
        if (mouseIsDown !== 0) {
            mouseIsDown = 0;
            var pos = getMousePos(canvas, eve);
            endX = pos.x;
            endY = pos.y;
            $("#x").val(startX);
            $("#y").val(startY);
            $("#width").val(endX - startX);
            $("#height").val(endY - startY);

            drawSquare(); //update on mouse-up
        }
    }

    function mouseDown(eve) {
        mouseIsDown = 1;
        var pos = getMousePos(canvas, eve);
        startX = endX = pos.x;
        startY = endY = pos.y;
        drawSquare(); //update
        $("#x").val(startX);
        $("#y").val(startY);

    }

    function mouseXY(eve) {

        if (mouseIsDown !== 0) {
            var pos = getMousePos(canvas, eve);
            endX = pos.x;
            endY = pos.y;
            $("#width").val(endX - startX);
            $("#height").val(endY - startY);

            drawSquare();
        }
    }

    function drawSquare() {
        // creating a square
        var w = endX - startX;
        var h = endY - startY;
        var offsetX = (w < 0) ? w : 0;
        var offsetY = (h < 0) ? h : 0;
        var width = Math.abs(w);
        var height = Math.abs(h);

        context.clearRect(0, 0, canvas.width, canvas.height);

        context.beginPath();
        context.rect(startX + offsetX, startY + offsetY, width, height);
        context.fillStyle = "yellow";
        context.fill();
        context.lineWidth = 7;
        context.strokeStyle = 'black';
        context.stroke();

    }

    function getMousePos(canvas, evt) {
        var rect = canvas.getBoundingClientRect();
        return {
            x: evt.clientX - rect.left,
            y: evt.clientY - rect.top
        };
    }
    var numDots = 0;
    var mediaName = "";
    init();

    $('#getCalibrationImages').submit(function() {
        $("#status").empty().text("File is uploading...");
        $(this).ajaxSubmit({
            error: function(xhr) {
                console.log('Error: ' + xhr.status);
            },
            success: function(response) {
                console.log(response);
                numDots = response.numDots;
                mediaName = response.filename;
                $("#mediaId").val(mediaName);
                $("#mediaId2").val(mediaName);
                $("#cols2").val($("#cols").val());
                $("#rows2").val($("#rows").val());

                $("#calibrationImgLink").attr("href", response.download);
                $("#calibrationImgBtn").removeClass("disabled").addClass("positive")
                //$("#status").empty().text(response);
            }
        });
        return false;
    });

    $('#uploadCamera').submit(function(e) {
        console.log(numDots)
        if ($("[name='cameraImgs']")[0].files.length != numDots + 1) {
            e.preventDefault();
            console.log("Bad request");
        } else {
            $("#status").empty().text("File is uploading...");
            $(this).ajaxSubmit({
                error: function(xhr) {
                    console.log('Error: ' + xhr.status);
                },
                success: function(response) {
                    console.log(response)
                    $("#cameraSuccess").show();
                    // put image received from response here
                }
            });
            return false;

        }
    });

    $('#warpMedia').submit(function(e) {
        $("#status").empty().text("File is uploading...");
        $(this).ajaxSubmit({
            error: function(xhr) {
                console.log('Error: ' + xhr.status);
            },
            success: function(response) {
                console.log(response)
                $("#finalImgLink").attr("href", response.download);
                $("#finalImgBtn").removeClass("disabled").addClass("positive")
                //$("#cameraSuccess").show();
                // put image received from response here
            }
        });
        return false;
    });
});
