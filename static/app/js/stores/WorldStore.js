import { Store } from 'flummox';
import Immutable from 'immutable';

import World from '../models/World';


export default class WorldStore extends Store {

    constructor({ worldActions }) {
        super();

        this.worldActions = worldActions;
        this.register(worldActions.getWorld, this.handleNewWorld);
        this.register(worldActions.updateWorld, this.handleNewWorld);
        this.state = {};
    }

    handleNewWorld(obj) {
        this.setState({
            world: new World(Immutable.fromJS(obj))
        });
    }

    getWorld() {
        if ( ! this.state.world) {
            this.worldActions.getWorld();
            return null;
        }

        return this.state.world;
    }
}
