import numeral from 'numeral';
import { capitalize, startCase } from 'lodash';


export default function toString(value, format) {
    if ( ! format) {
        format = typeof value;
    }

    switch (format) {
        case 'number':
            return numeral(value).format('0a');
        case 'float':
            return numeral(value).format('0.00');
        case 'percent':
            return numeral(value).format('0.0%');
        case 'time':
            return numeral(value).format('00:00:00');
        case 'key':
            return capitalize(startCase(value).toLowerCase());
        default:
            return value;
    }
}
