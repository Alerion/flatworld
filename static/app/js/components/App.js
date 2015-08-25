import FluxComponent from 'flummox/component';
import L from 'leaflet';
import React from 'react';


export default class App extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.map = null;
        this.regionsLayer = null;
        this.infoPanel = null;
        this.layersControl = null;
    }

    componentDidMount() {
        // Executed once after render. Here we don't have any information about the world.
        var config = {
            minZoom: 4,
            maxZoom: 7
        };
        this.map = L.map(React.findDOMNode(this.refs.map), config).setView([0, 0], 4);
        // FIXME: Should we clear up where is this initialized?
        L.tileLayer(CONFIG.TILE_LAYER_URL).addTo(this.map);

        // Add scale control
        L.control.scale({imperial: false}).addTo(this.map);

        // Add info panel
        this.infoPanel = L.control();

        this.infoPanel.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };

        this.infoPanel.update = function (region) {
            var content = '';
            if (region) {
                var cities = [];
                for (let city of region.cities) {
                    cities.push(<li key={city.id}>{city.name}: {city.stats.population}</li>);
                }

                content = <p>
                    <b>{region.name}</b>
                    <ul>{cities}</ul>
                </p>
            } else {
                content = <b>Hover over a regions</b>;
            }
            this._div.innerHTML = React.renderToString(content);
        };

        this.infoPanel.addTo(this.map);

        // Add layers control
        this.layersControl = L.control.layers({}, {}, {
            position: 'topleft',
            collapsed: false
        }).addTo(this.map);

        // Set world bounds
        // FIXME: Save them in DB for each world
        var southWest = L.latLng(-30, -30),
            northEast = L.latLng(30, 30),
            bounds = L.latLngBounds(southWest, northEast);
        this.map.setMaxBounds(bounds);
    }

    componentDidUpdate() {
        var world = this.props.world;

        // Render regions
        this.regionsLayer = L.geoJson(this.toGeoJSON(world.regions), {
            onEachFeature: (feature, layer) => {
                layer.on({
                    mouseover: this.highlightRegion.bind(this),
                    mouseout: this.resetHighlight.bind(this)
                });
            },
            style: function (feature) {
                return {
                    color: feature.properties.color,
                    weight: 0.5,
                    opacity: 0.8,
                    fillOpacity: 0.3
                };
            }
        });

        this.regionsLayer.addTo(this.map);
        this.layersControl.addOverlay(this.regionsLayer, 'Regions');

        // Render cities
        // TODO: Add resize on zoom. On large zoom level they are too small.

        var cities = [];
        for (let region of world.regions) {
            for (let city of region.cities) {
                cities.push(city);
            }
        }

        var citiesLayer = L.geoJson(this.toGeoJSON(cities, 'coords', {withColor: false}), {
            pointToLayer: function (feature, latlng) {
                var style = {
                    radius: 3,
                    fillColor: "#9E9E9E",
                    color: "#888",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                };

                if (feature.properties.capital) {
                    style.fillColor = '#FF5722';
                }

                return L.circleMarker(latlng, style);
            }
        });

        citiesLayer.addTo(this.map);
        this.layersControl.addOverlay(citiesLayer, 'Cities');
    }

    highlightRegion(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 4
        });

        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
        }

        this.infoPanel.update(layer.feature.properties);
    }

    resetHighlight(e) {
        this.regionsLayer.resetStyle(e.target);
        this.infoPanel.update();
    }

    toGeoJSON(data, field='geom', withColor=true) {
        var output = [];
        for (let item of data) {
            let properties = {};

            if (withColor) {
                properties.color = this.randomColor();
            }

            let obj = {
                type: "Feature",
                properties: Object.assign(properties, item),
                geometry: JSON.parse(item[field])
            }
            output.push(obj);
        }
        return output
    }

    randomColor() {
        // FIXME: Add more smart colors
        var r = Math.floor(Math.random() * 255);
        var g = Math.floor(Math.random() * 255);
        var b = Math.floor(Math.random() * 255);
        return "rgb("+r+" ,"+g+","+ b+")";
    }

    render() {
        // Set id to force componentDidUpdate
        // FIXME: Get height from screen size
        return (
            <div ref="map" className={"map"} id="{this.props.world.name}" style={{height: 840}}></div>
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
