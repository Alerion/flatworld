import {Store} from 'flummox';

import World from '../models/World';


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
        this.setState({
            world: World.fromJS(obj)
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
