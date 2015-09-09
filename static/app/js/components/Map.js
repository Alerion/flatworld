import FluxComponent from 'flummox/component';
import React from 'react';
import Map from '../map/Map';


class MapComponent extends React.Component {

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
        if (this.props.world) {
            this.map.setWorld(this.props.world);
        }
    }

    componentWillUnmount() {
        this.map.remove();
    }

    componentDidUpdate() {
        this.map.setWorld(this.props.world);
    }

    render() {
        // FIXME: Get height from screen size
        return (
            <div className="card">
                <div className="card-body">
                    <div ref="map" className="map" style={{height: 840}}></div>
                </div>
            </div>
        );
    }
}

// TODO: This part is similar for many components.
export default class FluxMapComponent extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                worldStore: store => ({
                    world: store.getWorld()
                })
            }}>
                <MapComponent {...this.props}/>
            </FluxComponent>
        );
    }

}
