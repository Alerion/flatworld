import { Actions } from 'flummox';


export default class WorldActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    async getWorld(worldId) {
        return await this.rpc.call('get_world', worldId);
    }
}
