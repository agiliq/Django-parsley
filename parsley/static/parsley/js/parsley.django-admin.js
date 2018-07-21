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
    });
}(window.jQuery || window.Zepto);
