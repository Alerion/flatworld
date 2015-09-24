'use strict';
// FIXME: This crap can't be imported so it is loaded with <script>.
// This module helps to reduce global variables in other modules.
/*global swal*/
export function confirm(config, callback) {
    config = Object.assign({
        showCancelButton: true,
        confirmButtonClass: 'btn-primary'
    }, config);

    swal(config, function(isConfirm) {
        if (isConfirm) {
            callback();
        }
    });
}

export function prompt(config, callback) {
    config = Object.assign({
        showCancelButton: true,
        closeOnConfirm: false,
        html: '<p><input /></p>',
    }, config);

    swal(config, function(isConfirm) {
        console.log(this);
        if (isConfirm) {
            callback();
        }
    });
}

export default swal;
