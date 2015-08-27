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
        return {
            color: feature.properties.color,
            weight: 1,
            opacity: 0.8,
            dashArray: '5 5',
            fillOpacity: 0
        };
    },

    onMouseover: function (e) {
        var layer = e.target;

        layer.setStyle({
            weight: 4
        });

        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
        }

        var regionId = layer.feature.properties.regionId;
        var regions = this.world.get('regions');
        this.infoPanel.show(regions.get(regionId));
    },

    onMouseout: function (e) {
        this.resetStyle(e.target);
        this.infoPanel.hide();
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
