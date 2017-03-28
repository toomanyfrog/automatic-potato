$(document).ready(function() {

    var numDots = 0;
    var mediaName = "";

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
                $("#calibrationImgLink").attr("href", response.download);
                $("#calibrationImgBtn").removeClass("disabled").addClass("positive")
                //$("#status").empty().text(response);
            }
        });
        return false;
    });

    $('#uploadCamera').submit(function(e) {
        console.log(numDots)
        if ($("[name='cameraImgs']")[0].files.length != numDots) {
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
});
