import {Store} from 'flummox';
import Immutable from 'seamless-immutable';


export default class UnitsStore extends Store {

    constructor({ actions }) {
        super();

        this.actions = actions;
        this.registerAsync(actions.getUnits, this.startLoading, this.updateUnits);

        this.state = {};
        this._loadingInProgress = false;
    }

    startLoading() {
        this._loadingInProgress = true;
    }

    updateUnits(obj) {
        this.setState({
            units: Immutable(obj)
        });
        this._loadingInProgress = false;
    }

    getUnits() {
        if ( ! this.state.units && ! this._loadingInProgress) {
            this.actions.getUnits();
            return null;
        }

        return this.state.units;
    }
}
