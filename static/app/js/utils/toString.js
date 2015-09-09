import numeral from 'numeral';


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
        default:
            return value;
    }
}
