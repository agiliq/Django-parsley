/*
 * Parsley.js - django admin helper
*/

!function ($) {
  'use strict';

  $( window ).on( 'load', function () {
    $( 'form' ).each( function () {
      $( this ).parsley({
          animate: false,
          errors: {
              errorsWrapper: '<ul class="errorlist"></ul>',
              container: function (element, isRadioOrCheckbox) {
                  return $("<div />").prependTo(element.closest(".form-row"));
              }
          },
          listeners: {
              onFieldError: function (element) {
                  var container = element.closest(".form-row");
                  if (container.not(".errors")) {
                      container.addClass("errors");
                  }
              }
          }
      });
    } );
  } );
}(window.jQuery || window.Zepto);
