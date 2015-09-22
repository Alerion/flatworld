'use strict';
import numeral from 'numeral';
import _ from 'lodash';


export default function toString(value, format) {
    if (! format) {
        format = typeof value;
    }

    switch (format) {
    case 'number':
        return numeral(value).format('0.[00]a');
    case 'int':
        return numeral(_.floor(value)).format('0.[00]a');
    case 'float':
        return numeral(value).format('0.00');
    case 'percent':
        return numeral(value).format('0.0%');
    case 'time':
        return numeral(value).format('00:00:00');
    case 'key':
        return _.capitalize(_.startCase(value).toLowerCase());
    default:
        return value;
    }
}
