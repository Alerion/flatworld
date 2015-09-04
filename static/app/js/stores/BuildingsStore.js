import {Store} from 'flummox';
import Immutable from 'immutable';


export default class WorldStore extends Store {

    constructor({ buildingsActions }) {
        super();

        this.buildingsActions = buildingsActions;
        this.registerAsync(
            buildingsActions.getBuildings, this.startBuildingsLoading, this.updateBuildings);

        this.state = {};
        this._loadingInProgress = false;
    }

    startBuildingsLoading() {
        this._loadingInProgress = true;
    }

    updateBuildings(obj) {
        this.setState({
            buildings: Immutable.fromJS(obj)
        });
        this._loadingInProgress = false;
    }

    getBuildings() {
        if ( ! this.state.buildings && ! this._loadingInProgress) {
            this.buildingsActions.getBuildings();
            return null;
        }

        return this.state.buildings;
    }
}
