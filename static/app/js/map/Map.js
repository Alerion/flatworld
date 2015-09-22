'use strict';
import L from 'leaflet';

import {RegionInfoPanel} from './controls';
import RegionsLayer from './layers/RegionsLayer';
import {CitiesLayer, CapitalsLayer, UserCityLayer} from './layers/CitiesLayer';

// Fix vector layer rendering when you drag
// From here https://github.com/Leaflet/Leaflet/issues/2814
L.Path.CLIP_PADDING = 0.75;


export default L.Map.extend({
    options: {
        minZoom: 4,
        maxZoom: 7,
        zoom: 4,
        center: [0, 0],
        attributionControl: false,
        // FIXME: Save them in DB for each world
        maxBounds: [[-40, -40], [40, 40]]
    },

    initialize: function(id, options) {
        L.Map.prototype.initialize.call(this, id, options);
        this.world = null;

        this.addLayer(L.tileLayer(CONFIG.TILE_LAYER_URL));

        // Initialize region info panel
        this.regionInfoPanel = new RegionInfoPanel();
        this.addControl(this.regionInfoPanel);

        // Layers
        this.regionsLayer = new RegionsLayer(this.regionInfoPanel);
        this.addLayer(this.regionsLayer);

        this.capitalsLayer = new CapitalsLayer();
        this.addLayer(this.capitalsLayer);

        this.userCityLayer = new UserCityLayer();
        this.addLayer(this.userCityLayer);

        this.citiesLayer = new CitiesLayer();
        // Events
        this.on('zoomend', this.onZoomend.bind(this));
    },

    setWorld: function(world) {
        this.world = world;

        this.eachLayer(function(layer) {
            if (layer.setWorld) {
                layer.setWorld(world);
            }
        });
    },

    getRelativeZoom: function() {
        // Used by layers for get style for zoom level. This is not absolute zoom,
        // so you can use to calculate styles and do not worry if world size,
        // zoom levels or scale can be changed.
        return (this.getZoom() - this.getMinZoom() + 1);
    },

    getPercentZoom: function() {
        return this.getRelativeZoom() / this.getMaxZoom();
    },

    onZoomend: function(event) {
        var zoom = this.getRelativeZoom();

        // FIXME: make some declarative way for this
        // FIXME: first time appears so long
        if (zoom >= 3) {
            this.addLayer(this.citiesLayer);
        } else {
            this.removeLayer(this.citiesLayer);
        }

        this.eachLayer(function(layer) {
            if (layer.updateStyle) {
                layer.updateStyle();
            }
        });
    }
});
