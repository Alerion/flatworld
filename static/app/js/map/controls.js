'use strict';
import L from 'leaflet';
import React from 'react';

import toString from '../utils/toString';


var InfoPanel = L.Control.extend({

    onAdd: function(map) {
        this.$container = $('<div class="info"></div>');
        this.hide();
        return this.$container[0];
    },

    show: function(obj) {
        this.$container.removeClass('hidden').html(this.renderObject(obj));
    },

    hide: function() {
        this.$container.addClass('hidden');
    },

    renderObject: function(obj) {
        return '';
    }
});


var RegionInfoPanel = InfoPanel.extend({

    renderObject: function(region) {
        return React.renderToStaticMarkup(<div>
            <b>{region.name}</b><br/>
            Population: {toString(region.totalPopulation())}<br/>
            Money: {toString(region.totalMoney())}<br/>
        </div>);
    }
});

export {InfoPanel, RegionInfoPanel};
