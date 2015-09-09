import Immutable from 'immutable';

var statsDefault = {
    population: null,
    population_growth: null,
    money: null,
    pasive_income: null,
    tax: null
}

class CityStats extends Immutable.Record(statsDefault) {

}

var defaults = {
    buildings: Immutable.Map(),
    capital: false,
    coords: null,
    id: null,
    name: null,
    region_id: null,
    stats: new CityStats(),
    user_id: null,
    world_id: null
}

export default class City extends Immutable.Record(defaults) {

}

City.fromJS = function (obj) {
    var imObj = Immutable.fromJS(Object.assign({}, obj, {
        stats: new CityStats(obj.stats)
    }));
    return new City(imObj);
}
