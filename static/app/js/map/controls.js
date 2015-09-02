import L from 'leaflet';
import React from 'react';
import $ from 'jquery';


var InfoPanel = L.Control.extend({

    onAdd: function (map) {
        this.$container = $('<div class="info"></div>');
        this.hide();
        return this.$container[0];
    },

    show: function (obj) {
        this.$container.removeClass('hidden').html(this.renderObject(obj));
    },

    hide: function () {
        this.$container.addClass('hidden');
    },

    renderObject: function (obj) {
        return '';
    }
});


var RegionInfoPanel = InfoPanel.extend({

    renderObject: function (region) {
        return React.renderToStaticMarkup(<div>
            <b>{region.get('name')}</b><br/>
            Population: {region.totalPopulation({verbose: true})}<br/>
            Money: {region.totalMoney({verbose: true})}<br/>
        </div>);
    }
});

export {InfoPanel, RegionInfoPanel};
