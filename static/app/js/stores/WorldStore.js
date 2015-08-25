import { Store } from 'flummox';

export default class WorldStore extends Store {

    constructor({ worldActions }) {
        super();

        this.worldActions = worldActions;
        this.register(worldActions.getWorld, this.handleNewWorld);
        this.state = {};
    }

    handleNewWorld(obj) {
        this.setState({
            world: obj
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
