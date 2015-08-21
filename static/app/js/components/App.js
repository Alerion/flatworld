import FluxComponent from 'flummox/component';
import React from 'react';

export default class App extends React.Component {

    constructor(props, context) {
        super(props, context);
    }

    render() {
        var world = this.props.world;

        if ( ! world) {
            return (<div>Loading...</div>);
        }

        return (
            <div>{world.name}</div>
        );
    }
}

export default class FluxApp extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                worldStore: store => ({
                    world: store.getWorld(this.props.worldId)
                })
            }}>
                <App />
            </FluxComponent>
        );
    }

}

export default FluxApp;
