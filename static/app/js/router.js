import React from 'react';
import Router from 'react-router';

var routes = [
    <Router.Route name="home" path="/world/:worldId/" handler={require('./components/App')} />
]

export default Router.create({
    routes: routes,
    location: Router.HistoryLocation
});
