import { Actions } from 'flummox';


export default class WorldActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
        this._pendingRequests = {};
    }

    getWorld() {
        return this.rpc.call('get_world');
    }

    updateWorld(world) {
        return world;
    }
}
