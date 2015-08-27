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
        var cities = [];

        for (let city of region.get('cities').values()) {
            cities.push(
                <li key={city.get('id')}>
                    {city.get('name')}({city.get('id')}): {city.get('stats').get('population')}
                </li>
            );
        }

        return React.renderToStaticMarkup(<p>
            <b>{region.get('name')}</b>
            <ul>{cities}</ul>
        </p>);
    }
});

export {InfoPanel, RegionInfoPanel};
