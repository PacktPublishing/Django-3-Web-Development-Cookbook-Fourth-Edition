$(function() {
  $("#id_picture_path").each(function() {
    $picture_path = $(this);
    if ($picture_path.val()) {
      $("#picture_preview").html(
        '<img src="' +
          window.settings.MEDIA_URL +
          "temporary-uploads/" +
          $picture_path.val() +
          '" alt="" class="img-fluid" />'
      );
    }
  });
  $("#id_picture").fileupload({
    dataType: "json",
    add: function(e, data) {
      $("#progress").css("visibility", "visible"); // show the progress bar
      data.submit(); // start uploading immediately
    },
    progressall: function(e, data) {
      var progress = parseInt((data.loaded / data.total) * 100, 10);
      $("#progress .progress-bar")
        .attr("aria-valuenow", progress)
        .css("width", progress + "%"); // show upload progress
    },
    done: function(e, data) {
      $.each(data.result.files, function(index, file) {
        $("#picture_preview").html(
          '<img src="' +
            window.settings.MEDIA_URL +
            "temporary-uploads/" +
            file.name +
            '" alt="" class="img-fluid" />'
        );
        $("#id_picture_path").val(file.name);
      });
      $("#progress").css("visibility", "hidden"); // hide progress bar
    }
  });
});
