import Immutable from 'immutable';
import numeral from 'numeral';

var defaults = {
    buildings: Immutable.Map(),
    capital: false,
    coords: null,
    id: null,
    name: null,
    region_id: null,
    stats: Immutable.Map(),
    user_id: null,
    world_id: null
}

export default class City extends Immutable.Record(defaults) {

    money(verbose=true) {
        var money = this.get('stats').get('money');

        if (verbose) {
            money = numeral(money).format('0');
        }

        return money;
    }

    population(verbose=true) {
        var population = this.get('stats').get('population');

        if (verbose) {
            population = numeral(population).format('0');
        }

        return population;
    }
}

City.fromJS = function (obj) {
    return new City(Immutable.fromJS(obj));
}
