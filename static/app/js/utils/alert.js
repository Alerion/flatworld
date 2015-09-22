'use strict';
// FIXME: This crap can't be imported so it is loaded with <script>.
// This module helps to reduce global variables in other modules.
/*global swal*/
var alert = swal;

export function confirm(config, callback) {
    config = Object.assign({
        showCancelButton: true,
        confirmButtonClass: 'btn-primary'
    }, config);

    alert(config, function(isConfirm) {
        if (isConfirm) {
            callback();
        }
    });
}

export default alert;
