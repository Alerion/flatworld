import L from 'leaflet';
import React from 'react';
import $ from 'jquery';
import jsx from '../utils/template';
import {InfoPanel, RegionInfoPanel} from './controls';
import RegionsLayer from './layers/RegionsLayer';

// Fix vector layer rendering when you drag
// From here https://github.com/Leaflet/Leaflet/issues/2814
L.Path.CLIP_PADDING = 1;

export default L.Map.extend({
    options: {
        minZoom: 4,
        maxZoom: 7,
        zoom: 4,
        center: [0, 0],
        attributionControl: false,
        // FIXME: Save them in DB for each world
        maxBounds: [[-35, -35], [35, 35]],
        layers: [
            L.tileLayer(CONFIG.TILE_LAYER_URL)
        ]
    },

    initialize: function (id, options) {
        L.Map.prototype.initialize.call(this, id, options);
        this.world = null;

        // Initialize region info panel
        this.regionInfoPanel = new RegionInfoPanel();
        this.addControl(this.regionInfoPanel);

        // Initialize layers control
        this.layersControl = L.control.layers({}, {}, {
            position: 'topleft',
            collapsed: false
        });
        this.addControl(this.layersControl);

        // Layers
        this.regionsLayer = new RegionsLayer(this.regionInfoPanel);
        this.addLayer(this.regionsLayer);
        this.layersControl.addOverlay(this.regionsLayer, 'Regions');

        this.citiesLayer = null;
    },

    setWorld: function (world) {
        var initialize = (! this.world);
        this.world = world;
        this.regionsLayer.setWorld(world);
        if (initialize) {
            // this.renderRegions();
            // this.renderCities();
        }
    },

    renderRegions: function () {
        var regions = this.world.get('regions').map(item => {
            return {
                type: "Feature",
                properties: {
                    color: randomColor(),
                    data: item
                },
                geometry: JSON.parse(item.get('geom'))
            }
        }).toArray();

        this.regionsLayer.addData(regions);
    },

    renderCities: function () {
        // TODO: Add resize on zoom. On large zoom level they are too small.
        var cities = [];
        for (let region of this.world.get('regions').values()) {
            for (let item of region.get('cities').values()) {
                cities.push({
                    type: "Feature",
                    properties: {
                        data: item
                    },
                    geometry: JSON.parse(item.get('coords'))
                })
            }
        }

        this.citiesLayer = L.geoJson(cities, {
            pointToLayer: function (feature, latlng) {
                var style = {
                    radius: 3,
                    fillColor: "#9E9E9E",
                    color: "#888",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                };

                if (feature.properties.data.get('capital')) {
                    style.fillColor = '#FF5722';
                }

                return L.circleMarker(latlng, style);
            }
        });

        this.addLayer(this.citiesLayer);
        this.layersControl.addOverlay(this.citiesLayer, 'Cities');
    }
});
