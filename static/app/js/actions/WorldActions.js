import { Actions } from 'flummox';


export default class WorldActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    async getWorld() {
        return await this.rpc.call('get_world');
    }

    updateWorld(world) {
        return world;
    }
}
