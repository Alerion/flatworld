import { Actions } from 'flummox';


export default class CityActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    getCity() {
        return this.rpc.call('get_city');
    }

    updateCity(city) {
        return city;
    }

    build(buildingId) {
        return this.rpc.call('build', buildingId);
    }
}
