$.fn.ready(function() {
    $(document).on('click', '.spoiler-btn', function (e) {
        e.preventDefault();
        $(this).parents(".spoiler-container")
               .find('.spoiler-body')
               .collapse('toggle');
    });
});

function scheduleScan(e, source, host) {
  $.get("scan/" + host, () => {
    var successBox = $("<div class='alert alert-success fade in'>\
        Scan successfully scheduled\
      </div>");
    $(source).parent().prepend(successBox);
    setTimeout(() => successBox.fadeOut(), 1000);
  });
  e.stopPropagation();
}
