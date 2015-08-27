import FluxComponent from 'flummox/component';
import L from 'leaflet';
import React from 'react';
import Map from '../map/Map';


export default class MapComponent extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.map = null;
        this.regionsLayer = null;
        this.infoPanel = null;
        this.layersControl = null;
    }

    componentDidMount() {
        // Executed once after render. Here we don't have any information about the world here.
        this.map = new Map(React.findDOMNode(this.refs.map));
    }

    componentDidUpdate() {
        this.map.setWorld(this.props.world);
    }

    render() {
        // FIXME: Get height from screen size
        return (
            <div ref="map" className={"map"}  style={{height: 840}}></div>
        );
    }
}


export default class FluxMapComponent extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                worldStore: store => ({
                    world: store.getWorld()
                })
            }}>
                <MapComponent />
            </FluxComponent>
        );
    }

}

export default FluxMapComponent;
