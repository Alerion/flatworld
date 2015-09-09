import {Store} from 'flummox';
import Immutable from 'immutable';

import City from '../models/City';


export default class CityStore extends Store {

    constructor({ cityActions }) {
        super();

        this.cityActions = cityActions;
        this.registerAsync(cityActions.getCity, this.startCityLoading, this.updateCity);
        this.register(cityActions.build, this.updateCity);
        this.register(cityActions.updateCity, this.updateCity);
        this.state = {};
        this._loadingInProgress = false;

        setInterval(this._updateBuildProgress.bind(this), 1000);
    }

    startCityLoading() {
        this._loadingInProgress = true;
    }

    updateCity(obj) {
        this.setState({
            city: City.fromJS(obj)
        });
        this._loadingInProgress = false;
    }

    getCity() {
        if ( ! this.state.city && ! this._loadingInProgress) {
            this.cityActions.getCity();
            return null;
        }

        return this.state.city;
    }

    _updateBuildProgress() {
        if ( ! this.state.city) return;

        var buildings = this.state.city.get('buildings').map(function (building) {
            if (building.get('in_progress') && building.get('build_progress') > 0) {
                return building.set('build_progress', building.get('build_progress') - 1);
            }
            return building;
        });

        this.setState({
            city: this.state.city.set('buildings', buildings)
        });
    }
}
