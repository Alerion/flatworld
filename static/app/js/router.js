var Marty = require('marty');
var React = require('react');
var Router = require('react-router');

var routes = [
    <Router.Route name="home" path="/world/:world_id/" handler={require('./components/home')} />
]

module.exports = Router.create({
    routes: routes,
    location: Router.HistoryLocation
});
