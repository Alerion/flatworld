import { Store } from 'flummox';
import Immutable from 'seamless-immutable';
import { mapValues, values } from 'lodash';


class Region {

    constructor(obj) {
        Object.assign(this, obj);
    }

    _totalForCities(field) {
        var total = 0;

        for (let city of values(this.cities)) {
            total += city.stats[field];
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


class World {

    constructor(obj) {
        Object.assign(this, obj);
        this.regions = mapValues(this.regions, function(value) {
            return Immutable(new Region(value), {prototype: Region.prototype});
        });
    }

    *getAllCities() {
        for (let region of values(this.regions)) {
            for (let city of values(region.cities)) {
                yield city;
            }
        }
    }

    _totalForCities(field) {
        var total = 0;

        for (let city of this.getAllCities()) {
            total += city.stats[field];
        }

        return total;
    }

    totalPopulation(verbose=true) {
        return this._totalForCities('population');
    }

    totalMoney(verbose=true) {
        return this._totalForCities('money');
    }
}


export default class WorldStore extends Store {

    constructor({ actions }) {
        super();

        this.actions = actions;
        this.registerAsync(actions.getWorld, this.startLoading, this.updateWorld);
        this.register(actions.updateWorld, this.updateWorld);
        this.state = {};
        this._loadingInProgress = false;
    }

    startLoading() {
        this._loadingInProgress = true;
    }

    updateWorld(obj) {
        var world = Immutable(new World(obj), {prototype: World.prototype});
        this.setState({
            world: world
        });
        this._loadingInProgress = false;
    }

    getWorld() {
        if ( ! this.state.world && ! this._loadingInProgress) {
            this.actions.getWorld();
            return null;
        }

        return this.state.world;
    }
}
