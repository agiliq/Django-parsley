/*
 * Parsley.js - django admin helper
*/

!function ($) {
  'use strict';

  $( window ).on( 'load', function () {
    $( 'form' ).each( function () {
      $( this ).parsley({
      });
    } );
  } );
}(window.jQuery || window.Zepto);
