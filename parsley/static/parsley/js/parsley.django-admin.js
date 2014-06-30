/*
 * Django admin helper for Parsley.js.
 *
 * This calls `parsley` for all forms, and sets up event listeners
 * to handle success and errors on field validation.
 *
 * It supports [django-grappelli](https://github.com/sehmaschine/django-grappelli).
 */

(function ($) {
  'use strict';

  $( window ).on( 'load', function () {
    var is_grappelli = $('#grp-container').length;
    var form_selector = is_grappelli ? '.grp-change-form form' : '.change-form form';
    var row_selector = is_grappelli ? '.grp-row' : '.form-row';

    $( form_selector ).each( function () {
      $( this ).parsley({
          errorsWrapper: '<ul class="errorlist"></ul>',
          errorsContainer: function (field) {
            if (is_grappelli) {
              // Grappelli appends the errors to the field.
              return;
            }
            return $("<div />").prependTo(
              field.$element.closest(".form-row"));
          }
      }).subscribe('parsley:field:error', function (field) {
          var container = field.$element.closest(row_selector);
          console.log(container);
          container.addClass("errors grp-errors");
      }).subscribe('parsley:field:success', function (field) {
          var container = field.$element.closest(row_selector);
          container.removeClass("errors grp-errors");
      });
    } );
  } );
})(window.jQuery || window.Zepto);
