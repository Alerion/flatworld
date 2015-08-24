import FluxComponent from 'flummox/component';
import Leaflet from 'leaflet';
import React from 'react';


export default class App extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.map = null;
    }

    componentDidMount() {
        // Executed once after render. Here we don't have any information about the world.
        this.map = Leaflet.map(React.findDOMNode(this.refs.map)).setView([0, 0], 4);
        Leaflet.tileLayer(CONFIG.TILE_LAYER_URL).addTo(this.map);
    }

    componentDidUpdate() {
        // Executed when we get information about the world.
        var world = this.props.world;
        var regionsLayer = L.layerGroup();

        for (let region of world.regions) {
            var item = L.geoJson(JSON.parse(region.geom), {
                style: function (feature) {
                    var color;
                    var r = Math.floor(Math.random() * 255);
                    var g = Math.floor(Math.random() * 255);
                    var b = Math.floor(Math.random() * 255);
                    color= "rgb("+r+" ,"+g+","+ b+")";
                    return {
                        color: color,
                        "weight": 0.5,
                        "opacity": 0.8
                    };
                }
            });
            regionsLayer.addLayer(item);
        }

        regionsLayer.addTo(this.map);

        var overlayMaps = {
            'Regions': regionsLayer
        }
        L.control.layers({}, overlayMaps).addTo(this.map);
    }

    toGeoJSON(data) {
        var geoJSON = [];
    }

    render() {
        // Set id to force componentDidUpdate
        // FIXME: Get height from screen size
        return (
            <div ref="map" id="{this.props.world.name}" style={{height: 840}}></div>
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
