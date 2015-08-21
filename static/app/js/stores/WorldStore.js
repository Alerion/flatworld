import { Store } from 'flummox';

export default class WorldStore extends Store {

    constructor({ worldActions }) {
        super();

        this.worldActions = worldActions;
        this.register(worldActions.getWorld, this.handleNewWorld);
        this.state = {};
    }

    handleNewWorld(obj) {
        console.log('New world:', obj);
        this.setState({
            [obj.id]: obj
        });
    }

    getWorld(worldId) {
        if ( ! this.state[worldId]) {
            console.log('Cant find world with ID', worldId);
            this.worldActions.getWorld(worldId);
            return null;
        }

        return this.state[worldId];
    }
}
