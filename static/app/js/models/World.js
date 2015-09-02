import Immutable from 'immutable';
import numeral from 'numeral';

import Region from './Region';

var defaults = {
    id: null,
    name: null,
    created: null,
    params: Immutable.Map(),
    regions: Immutable.Map()
};


export default class World extends Immutable.Record(defaults) {

    *getAllCities() {
        for (let region of this.get('regions').values()) {
            for (let city of region.get('cities').values()) {
                yield city;
            }
        }
    }

    _totalForCities(field, verbose=false) {
        var total = 0;

        for (let city of this.getAllCities()) {
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

World.fromJS = function (obj) {
    var imObj = Immutable.fromJS(obj);

    var regions = imObj.get('regions').withMutations(function (regions) {
        for (let [key, region] of regions) {
            regions.set(key, new Region(region));
        }
    });

    imObj = imObj.set('regions', regions);

    return new World(imObj);
}
