'use strict';
import { Actions } from 'flummox';


export default class UnitsActions extends Actions {

    constructor({ rpc }) {
        super();
        this.rpc = rpc;
    }

    getUnits() {
        return this.rpc.call('get_units');
    }
}
