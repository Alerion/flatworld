'use strict';
import { Actions } from 'flummox';


export default class QuestsActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    getQuests() {
        return this.rpc.call('get_quests');
    }

    updateQuests(quests) {
        return quests;
    }
}
