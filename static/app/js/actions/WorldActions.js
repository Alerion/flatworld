import { Actions } from 'flummox';


export default class WorldActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    getWorld() {
        return this.rpc.call('get_world');
    }

    updateWorld(world) {
        return world;
    }
}
