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
}
