import { Store } from 'flummox';
import Immutable from 'seamless-immutable';


export default class BuildingsStore extends Store {

    constructor({ actions }) {
        super();

        this.actions = actions;
        this.registerAsync(actions.getBuildings, this.startLoading, this.updateBuildings);

        this.state = {};
        this._loadingInProgress = false;
    }

    startLoading() {
        this._loadingInProgress = true;
    }

    updateBuildings(obj) {
        this.setState({
            buildings: Immutable(obj)
        });
        this._loadingInProgress = false;
    }

    getBuildings() {
        if ( ! this.state.buildings && ! this._loadingInProgress) {
            this.actions.getBuildings();
            return null;
        }

        return this.state.buildings;
    }
}
