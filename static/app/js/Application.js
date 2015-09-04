import { Flux } from 'flummox';

import BuildingsActions from './actions/BuildingsActions';
import CityActions from './actions/CityActions';
import WorldActions from './actions/WorldActions';

import BuildingsStore from './stores/BuildingsStore';
import CityStore from './stores/CityStore';
import WorldStore from './stores/WorldStore';

import Rpc from './Rpc';


export default class Application extends Flux {

    constructor(rpc) {
        super();
        this.rpc = rpc;

        const worldActions = this.createActions('worldActions', WorldActions, { rpc });
        this.createStore('worldStore', WorldStore, { worldActions });

        const buildingsActions = this.createActions('buildingsActions', BuildingsActions, { rpc });
        this.createStore('buildingsStore', BuildingsStore, { buildingsActions });

        const cityActions = this.createActions('cityActions', CityActions, { rpc });
        this.createStore('cityStore', CityStore, { cityActions });

        rpc.subscribe('update:world', (world, topic) => {
            this.getActions('worldActions').updateWorld(world);
        });
    }
}
