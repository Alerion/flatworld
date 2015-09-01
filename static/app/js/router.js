import React from 'react';
import Router from 'react-router';

var routes = (
    <Router.Route handler={require('./components/App')}>
        <Router.Route name="home" path="/world/:worldId/" handler={require('./components/Map')} />
    </Router.Route>
)

export default Router.create({
    routes: routes,
    location: Router.HistoryLocation
});
