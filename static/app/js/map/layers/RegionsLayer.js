// FIXME: We need better way to get style for zoom level, and better way to update them.
var STYLE_DEFAULT = function (zoom) {
    var dash = 5 * zoom;
    return {
        weight: 2 * zoom,
        opacity: 0.8,
        dashArray: `${dash} ${dash}`,
        fillOpacity: 0
    }
};

var STYLE_HIGHLIGHT = function (zoom) {
    var dash = 8 * zoom;
    return {
        weight: 4 * zoom,
        dashArray: `${dash} ${dash}`
    }
};

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
                        color: randomColor(),
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
        return Object.assign({}, {
            color: feature.properties.color,
        }, STYLE_DEFAULT(this._map.getRelativeZoom()));
    },

    onMouseover: function (event) {
        var layer = event.target;

        layer.highligh = true;
        layer.setStyle(STYLE_HIGHLIGHT(this._map.getRelativeZoom()));

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
        // Set what this.style returns.
        this.eachLayer(function (layer) {
            if (layer.highligh) {
                layer.setStyle(STYLE_HIGHLIGHT(this._map.getRelativeZoom()));
            } else {
                this.resetStyle(layer);
            }
        }, this);
    }
});


function randomColor() {
    // FIXME: Add more smart colors
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgb("+r+" ,"+g+","+ b+")";
}

export default RegionsLayer;
