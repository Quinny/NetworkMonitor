$.fn.ready(function() {
    // Spoiler
    $(document).on('click', '.spoiler-btn', function (e) {
        e.preventDefault()
        $(this).parent().children('.spoiler-body').collapse('toggle')
    });
});

function scheduleScan(source, host) {
  $.get("scan/" + host, () => {
    var successBox = $("<div class='alert alert-success fade in'>\
        Scan successfully scheduled\
      </div>");
    $(source).parent().prepend(successBox);
    setTimeout(() => successBox.fadeOut(), 1000);
  });
  e.stopPropagation();
}
