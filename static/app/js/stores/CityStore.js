import { Store } from 'flummox';
import Immutable from 'seamless-immutable';
import { map, forIn, isEmpty } from 'lodash';


export default class CityStore extends Store {

    constructor({ actions }) {
        super();

        this.actions = actions;
        this.registerAsync(actions.getCity, this.startLoading, this.updateCity);
        this.register(actions.build, this.updateCity);
        this.register(actions.updateCity, this.updateCity);
        this.state = {};
        this._loadingInProgress = false;

        setInterval(this._updateBuildProgress.bind(this), 1000);
    }

    startCityLoading() {
        this._loadingInProgress = true;
    }

    updateCity(obj) {
        this.setState({
            city: Immutable(obj)
        });
        this._loadingInProgress = false;
    }

    getCity() {
        if ( ! this.state.city && ! this._loadingInProgress) {
            this.actions.getCity();
            return null;
        }

        return this.state.city;
    }

    _updateBuildProgress() {
        if ( ! this.state.city) return;

        var updates = {};
        forIn(this.state.city.buildings, function(building, id) {
            if (building.in_progress && building.build_progress > 0) {
                updates[id] = {
                    build_progress: building.build_progress - 1
                }
            }
        });

        if ( ! isEmpty(updates)) {
            var buildings = this.state.city.buildings.merge(updates, {deep: true});
            // FIXME: Do not update whole city.
            this.setState({
                city: this.state.city.merge({buildings: buildings})
            });
        }
    }
}
