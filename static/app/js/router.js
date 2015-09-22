'use strict';
import React from 'react';
import Router from 'react-router';

var routes = (
    <Router.Route handler={require('./components/App')}>
        <Router.Route
            name="world"
            path="/world/:worldId/"
            handler={require('./components/Map')}
            />
        <Router.Route
            name="building"
            path="/world/:worldId/building/"
            handler={require('./components/Buildings')}
            />
        <Router.Route
            name="units"
            path="/world/:worldId/units/"
            handler={require('./components/Units')}
            />
        <Router.Route
            name="quest-demo"
            path="/world/:worldId/quest-demo/"
            handler={require('./components/QuestDemo')}
            />
    </Router.Route>
);

export default Router.create({
    routes: routes,
    location: Router.HistoryLocation
});
