import Immutable from 'immutable';
import numeral from 'numeral';

var defaults = {
    id: null,
    name: null,
    cities: Immutable.Map(),
    geom: null,
    neighbors: Immutable.List(),
    params: Immutable.Map()
};


export default class Region extends Immutable.Record(defaults) {

    _totalForCities(field, verbose=false) {
        var total = 0;

        for (let city of this.get('cities').values()) {
            total += city.get('stats').get(field);
        }

        if (verbose) {
            total = numeral(total).format('0,0');
        }

        return total;
    }

    totalPopulation(verbose=false) {
        return this._totalForCities('population', verbose);
    }

    totalMoney(verbose=false) {
        return this._totalForCities('money', verbose);
    }
}
