'use strict';
import L from 'leaflet';
import _ from 'lodash';


var BaseCitiesLayer = L.GeoJSON.extend({
    iconUrl: null,

    initialize: function(geojson, options) {
        L.GeoJSON.prototype.initialize.call(this, geojson, options);

        this.world = null;
        this.options.pointToLayer = this.pointToLayer.bind(this);
        this.options.filter = this.filter.bind(this);
    },

    setWorld: function(world) {
        var init = (! this.world);
        this.world = world;
        // Render region on first world load. Later we do not need re-render them,
        // because they really never change, just data.
        if (init) {
            var cities = [];
            for (const region of _.values(world.regions)) {
                for (const city of _.values(region.cities)) {
                    cities.push({
                        type: 'Feature',
                        properties: {
                            capital: city.capital,
                            userId: city.user_id,
                            cityId: city.id,
                            regionId: region.id
                        },
                        geometry: JSON.parse(city.coords)
                    });
                }
            }

            this.addData(cities);
        }
    },

    getIcon: function(zoom) {
        zoom = 0.6 + 0.9 * zoom;
        return L.icon({
            iconUrl: this.iconUrl,
            iconSize: [32 * zoom, 37 * zoom]
        });
    },

    pointToLayer: function(feature, latlng) {
        var cityId = feature.properties.cityId;
        var regionId = feature.properties.regionId;
        var city = this.world.regions[regionId].cities[cityId];

        // FIXME: Add popup with details on click
        var marker = L.marker(latlng, {
            icon: this.getIcon(this._map.getPercentZoom()),
            title: city.name
        });

        return marker;
    },

    updateStyle: function() {
        var zoom = this._map.getPercentZoom();
        // Set what this.style returns.
        this.eachLayer(function(layer) {
            layer.setIcon(this.getIcon(zoom));
        }, this);
    },

    filter: function(feature, layer) {
        return true;
    }
});

var CapitalsLayer = BaseCitiesLayer.extend({
    iconUrl: CONFIG.STATIC_URL + 'img/map/icons/purple/castle-2.png',

    filter: function(feature, layer) {
        return feature.properties.capital;
    }
});

var CitiesLayer = BaseCitiesLayer.extend({
    iconUrl: CONFIG.STATIC_URL + 'img/map/icons/bluegray/smallcity.png',

    filter: function(feature, layer) {
        return ! feature.properties.capital && feature.properties.userId != CONFIG.USER_ID;
    }
});

var UserCityLayer = BaseCitiesLayer.extend({
    iconUrl: CONFIG.STATIC_URL + 'img/map/icons/deeporange/palace-2.png',

    filter: function(feature, layer) {
        return feature.properties.userId == CONFIG.USER_ID;
    }
});

export {CapitalsLayer, CitiesLayer, UserCityLayer};
