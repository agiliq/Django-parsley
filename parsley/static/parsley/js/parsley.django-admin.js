/*
 * Parsley.js - django admin helper
 */
! function($) {
    'use strict';

    $(window).on('load', function() {
        // Don't parsleyfy Django search boxes. It breaks layout
        $('form:not(#changelist-search, #changelist-form)').each(function() {
            $(this).parsley({});
        });
        // Move parsley-errors-list after help elements because it looks less broken.
        $('.parsley-errors-list + .help').each(function() {
            $(this).after($(this).prev());
        });
    });
}(window.jQuery || window.Zepto);
