import { Actions } from 'flummox';


export default class WorldActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
        this._pendingRequests = {};
    }

    async getWorld() {
        if ( ! this._pendingRequests[this.getWorld._id]) {
            var promise = this.rpc.call('get_world');
            this._pendingRequests[this.getWorld._id] = promise;
        }
        var result = await this._pendingRequests[this.getWorld._id];
        delete this._pendingRequests[this.getWorld._id];
        return result;
    }

    updateWorld(world) {
        return world;
    }
}
