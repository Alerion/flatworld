'use strict';
import _ from 'lodash';
import moment from 'moment';
import numeral from 'numeral';


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
    case 'fromDate':
        return moment(value).fromNow();
    default:
        return value;
    }
}
