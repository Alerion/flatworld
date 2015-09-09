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

    _totalForCities(field) {
        var total = 0;

        for (let city of this.get('cities').values()) {
            total += city.get('stats').get(field);
        }

        return total;
    }

    totalPopulation() {
        return this._totalForCities('population');
    }

    totalMoney() {
        return this._totalForCities('money');
    }
}
