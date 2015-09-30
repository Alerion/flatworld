'use strict';
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

    startQuest(questId) {
        return this.rpc.call('start_quest', questId);
    }

    closeQuest(questId) {
        return this.rpc.call('close_quest', questId);
    }
}
