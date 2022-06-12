// page init
jQuery(function(){
	initMasonry();
	initMobileNav();
});

// masonry init
function initMasonry() {
	jQuery(window).on('load masonry/refresh', function() {
                jQuery('.js-masonry').masonry('layout');
        });
}

// mobile menu init
function initMobileNav() {
	jQuery('body').mobileNav({
		hideOnClickOutside: true,
		menuActiveClass: 'nav-active',
		menuOpener: '.nav-opener',
		menuDrop: '.nav-drop'
	});
}
