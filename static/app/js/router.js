var Marty = require('marty');
var React = require('react');
var Router = require('react-router');

var routes = [
  <Router.Route name="home" path="/" handler={require('./components/home')} />
]

module.exports = Router.create({
  routes: routes,
  location: location()
});

function location() {
  if (typeof window !== 'undefined') {
    return Router.HistoryLocation;
  }
}
