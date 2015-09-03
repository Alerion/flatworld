import { Flux } from 'flummox';

import WorldActions from './actions/WorldActions'
import BuildingsActions from './actions/BuildingsActions'

import WorldStore from './stores/WorldStore'
import BuildingsStore from './stores/BuildingsStore'

import Rpc from './Rpc'


export default class Application extends Flux {

    constructor(rpc) {
        super();
        this.rpc = rpc;

        const worldActions = this.createActions('worldActions', WorldActions, { rpc });
        this.createStore('worldStore', WorldStore, { worldActions });

        const buildingsActions = this.createActions('buildingsActions', BuildingsActions, { rpc });
        this.createStore('buildingsStore', BuildingsStore, { buildingsActions });

        rpc.subscribe('update:world', (world, topic) => {
            this.getActions('worldActions').updateWorld(world);
        });
    }
}
