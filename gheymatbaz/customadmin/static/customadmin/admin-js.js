$(document).ready(function () {
    $('.show-more-category').on('click', function () {
        $(this).parent().next("ul").slideDown();

    })
});