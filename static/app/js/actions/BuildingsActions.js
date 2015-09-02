import { Actions } from 'flummox';


export default class BuildingsActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    getBuildings() {
        return this.rpc.call('get_buildings');
    }
}
