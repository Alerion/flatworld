import { Flux } from 'flummox';
import WorldActions from './actions/WorldActions'
import WorldStore from './stores/WorldStore'
import Rpc from './Rpc'


export default class AppFlux extends Flux {

    constructor(rpc) {
        super();
        this.rpc = rpc;
        const worldActions = this.createActions('worldActions', WorldActions, { rpc });
        this.createStore('worldStore', WorldStore, { worldActions });

        rpc.subscribe('update:world', (world, topic) => {
            this.getActions('worldActions').updateWorld(world);
        });
    }
}
