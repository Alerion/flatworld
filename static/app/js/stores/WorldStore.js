import { Store } from 'flummox';

import World from '../models/World';


export default class WorldStore extends Store {

    constructor({ worldActions }) {
        super();

        this.worldActions = worldActions;
        this.registerAsync(worldActions.getWorld, this.startWorldLoading, this.updateWorld);
        this.register(worldActions.updateWorld, this.updateWorld);
        this.state = {};
        this._loadingInProgress = false;
    }

    startWorldLoading() {
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
            this.worldActions.getWorld();
            return null;
        }

        return this.state.world;
    }
}
