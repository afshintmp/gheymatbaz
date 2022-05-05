$(document).ready(function () {
    $('.show-more-category').on('click', function () {
            if ($(this).parent().next("ul:hidden").length) {
                $(this).addClass('show-more-category-rotate').parent().next("ul").slideDown('fast');
            } else {
                $(this).removeClass('show-more-category-rotate').parent().next("ul").slideUp('fast');
                $(this).parent().next("ul").find('ul').slideUp('fast');
                $(this).parent().next("ul").find('span').removeClass('show-more-category-rotate');
            }
        }
    )
    $('#connector').on('change', function () {

        $('#category-tree input').prop('checked', false);

        selectVal = $(this).val();

        selectVal.forEach(elem => {
                $("input[value=" + elem + "]").prop('checked', true);
                $("input[value=" + elem + "]").parents('ul').slideDown();
                $("input[value=" + elem + "]").parents('ul').prev('li').find('span').addClass('show-more-category-rotate');

                // par.forEach(p=>{
                //     console.log(p)
                // })
                // console.log(parent)
            }
        )

    })
});
