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
                $("#calibrationSuccess").show();
                //$("#status").empty().text(response);
            }
        });
        return false;
    });

    $('#uploadForm').submit(function() {
        $("#status").empty().text("File is uploading...");
        $(this).ajaxSubmit({
            error: function(xhr) {
                console.log('Error: ' + xhr.status);
            },
            success: function(response) {
                console.log(response)
                $("#status").empty().text(response);
            }
        });
        return false;
    });
});
