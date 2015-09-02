import L from 'leaflet';

// FIXME: We need better way to get style for zoom level, and better way to update them.
var STYLE_DEFAULT = function (zoom) {
    var dash = 24 * zoom;
    return {
        weight: 12 * zoom,
        opacity: 0.8,
        color: '#9E9E9E',
        dashArray: `${dash} ${dash}`,
        fillOpacity: 0
    }
};

var STYLE_HIGHLIGHT = function (zoom) {
    var dash = 32 * zoom;
    return {
        weight: 16 * zoom,
        color: '#607D8B',
        dashArray: `${dash} ${dash}`
    }
};

// FIXME: Memory somewhere here
var RegionsLayer = L.GeoJSON.extend({

    initialize: function (infoPanel, geojson, options) {
        L.GeoJSON.prototype.initialize.call(this, geojson, options);

        this.world = null;
        this.infoPanel = infoPanel;
        this.options.onEachFeature = this.onEachFeature.bind(this);
        this.options.style = this.style.bind(this);
    },

    setWorld: function (world) {
        // Render region on first world load. Later we do not need re-render them,
        // because they really never change, just data.
        if ( ! this.world) {
            var regions = world.get('regions').map(item => {
                return {
                    type: "Feature",
                    properties: {
                        regionId: String(item.get('id'))
                    },
                    geometry: JSON.parse(item.get('geom'))
                }
            }).toArray();

            this.addData(regions);
        }

        this.world = world;
    },

    onEachFeature: function (feature, layer) {
        layer.on({
            mouseover: this.onMouseover.bind(this),
            mouseout: this.onMouseout.bind(this)
        });
    },

    style: function (feature) {
        return STYLE_DEFAULT(this._map.getPercentZoom());
    },

    onMouseover: function (event) {
        var layer = event.target;

        layer.highligh = true;
        layer.setStyle(STYLE_HIGHLIGHT(this._map.getPercentZoom()));

        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
        }

        var regionId = layer.feature.properties.regionId;
        this.infoPanel.show(this.world.get('regions').get(regionId));
    },

    onMouseout: function (event) {
        var layer = event.target;
        delete layer.highligh;
        this.resetStyle(layer);
        this.infoPanel.hide();
    },

    updateStyle: function () {
        var zoom = this._map.getPercentZoom();
        // Set what this.style returns.
        this.eachLayer(function (layer) {
            if (layer.highligh) {
                layer.setStyle(STYLE_HIGHLIGHT(zoom));
            } else {
                this.resetStyle(layer);
            }
        }, this);
    }
});

export default RegionsLayer;
