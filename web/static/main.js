$.fn.ready(function() {
    // Spoiler
    $(document).on('click', '.spoiler-btn', function (e) {
        e.preventDefault()
        $(this).parent().children('.spoiler-body').collapse('toggle')
    });
});

function scheduleScan(source, host) {
  $.get("scan/" + host, () => {
    $(source).prepend(
        "<div class='alert alert-success fade in alert-dismissable'>\
          Scan successfully scheduled\
        </div>"
    );
  });
}
