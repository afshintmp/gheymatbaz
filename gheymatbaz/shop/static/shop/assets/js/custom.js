$(document).ready(function() {
    $('.js-example-basic-single').select2({
        dir:'rtl',
    });
});


$('.btn-show-category').click(function (){
    $('.category-popup').addClass('show')
    $('.category-popup .category-main-bar').show()
    $('.category-popup .profile-main-bar').hide()
    $('body').addClass('before-black')
})
$('.btn-show-profile').click(function (){
    $('.category-popup').addClass('show')
    $('.category-popup .category-main-bar').hide()
    $('.category-popup .profile-main-bar').show()
    $('body').addClass('before-black')
})
$('.btn-show-profile').click(function (){
    $('.category-popup').addClass('show')
    $('.category-popup .category-main-bar').hide()
    $('.category-popup .profile-main-bar').show()
    $('body').addClass('before-black')
})
$('.btn-show-sort').click(function (){
    $('.category-popup').addClass('show')
    $('.category-popup .category-main-bar').hide()
    $('.category-popup .profile-main-bar').hide()
    $('.category-popup .sort-main-bar').show()
    $('body').addClass('before-black')
})
$('.category-popup .btn-close').click(function (){
    $('.category-popup').removeClass('show')
    $('body').removeClass('before-black')
})

$(".scroll").mCustomScrollbar({
    axis:"y" // horizontal scrollbar
});

$('.drop-down-toggle').click(function (){
    $(this).toggleClass('active').parent().find('.drop-down-menu').slideToggle()
})


$('.show-result').focus(function (){
    $(this).addClass('active')
    $(this).parent().parent().find('.search-result').slideDown()
})
$('.show-result').blur(function (){
    $(this).removeClass('active')
    $(this).parent().parent().find('.search-result').slideUp()
})

$('.show-result-mobile').click(function (){
    $('.search-popup').addClass('show')
})
$('.search-popup .btn-close').click(function (){
    $('.search-popup').removeClass('show')
})




var swipercategory = new Swiper('.swiper-category', {
    spaceBetween: 30,
    slidesPerView: 'auto',
    freeMode:true,
    pagination: {
        el: '.swiper-pagination-category',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-category',
        prevEl: '.swiper-button-prev-category',
    },
    breakpoints: {
        768 : {
            spaceBetween: 20,
        },
    }
});

var swipersearchresults = new Swiper('.swiper-search-results', {
    spaceBetween: 10,
    slidesPerView: 'auto',
    freeMode:true,
    pagination: {
        el: '.swiper-pagination-search-results',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-search-results',
        prevEl: '.swiper-button-prev-search-results',
    },
});
var swiperbrands = new Swiper('.swiper-brands', {
    spaceBetween: 15,
    slidesPerView: 'auto',
    loop: false,
    freeMode:true,
    pagination: {
        el: '.swiper-pagination-brands',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-brands',
        prevEl: '.swiper-button-prev-brands',
    },
    breakpoints: {
        992 : {
            loop: false,
        },
    }
});

var swiperp1 = new Swiper('.swiper-p-1', {
    spaceBetween: 15,
    slidesPerView: 4,
    pagination: {
        el: '.swiper-pagination-p-1',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-p-1',
        prevEl: '.swiper-button-prev-p-1',
    },
    breakpoints: {
        992 : {
            slidesPerView: 'auto',
            loop: false,
            freeMode:true,
        },
        1500 : {
            slidesPerView: 3,
        },
    }
});
var swiperp2 = new Swiper('.swiper-p-2', {
    spaceBetween: 15,
    slidesPerView: 4,
    pagination: {
        el: '.swiper-pagination-p-2',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-p-2',
        prevEl: '.swiper-button-prev-p-2',
    },
    breakpoints: {
        992 : {
            slidesPerView: 'auto',
            loop: false,
            freeMode:true,
        },
        1500 : {
            slidesPerView: 3,
        },
    }
});

var swiperp3 = new Swiper('.swiper-p-3', {
    spaceBetween: 15,
    slidesPerView: 5,
    pagination: {
        el: '.swiper-pagination-p-3',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-p-3',
        prevEl: '.swiper-button-prev-p-3',
    },
    breakpoints: {
        992 : {
            slidesPerView: 'auto',
            loop: false,
            freeMode:true,
        },
        1200 : {
            slidesPerView: 3,
        },
        1500 : {
            slidesPerView: 4,
        },
    }
});

var swiperp4 = new Swiper('.swiper-p-4', {
    spaceBetween: 15,
    slidesPerView: 5,
    pagination: {
        el: '.swiper-pagination-p-4',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-p-4',
        prevEl: '.swiper-button-prev-p-4',
    },
    breakpoints: {
        992 : {
            slidesPerView: 'auto',
            loop: false,
            freeMode:true,
        },
        1200 : {
            slidesPerView: 3,
        },
        1500 : {
            slidesPerView: 4,
        },
    }
});





var thumbsyncsswiperp = new Swiper('.swiper-sync-p', {
    spaceBetween: 15,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesVisibility: true,
    watchSlidesProgress: true,
    breakpoints: {
        450: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1200: {
            slidesPerView: 4,
        },
        1450: {
            slidesPerView: 3,
        },
    }
});
var mainsyncswiperp = new Swiper('.swiper-main-p', {
    spaceBetween: 0,
    zoom: true,
    loop:true,
    loopedSlides: 1, //looped slides should be the same
    navigation: {
        nextEl: '.swiper-button-next-main-p',
        prevEl: '.swiper-button-prev-main-p',
    },
    pagination: {
        // el: '.swiper-pagination-main-sync',
        // clickable:true,

    },
    thumbs: {
        swiper: thumbsyncsswiperp,
    },
});



var swipershop = new Swiper('.swiper-shop', {
    spaceBetween: 10,
    slidesPerView: 4,
    pagination: {
        el: '.swiper-pagination-shop',
        clickable:true,
    },
    navigation: {
        nextEl: '.swiper-button-next-shop',
        prevEl: '.swiper-button-prev-shop',
    },
    breakpoints: {
        992 : {
            slidesPerView: 'auto',
            loop: false,
            freeMode:true,
        },
        1500 : {
            slidesPerView: 3,
        },
    }
});
if (window.innerWidth > 992) {
    swipershop.destroy();
}