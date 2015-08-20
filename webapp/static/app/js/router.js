var Marty = require('marty');
var Router = require('react-router');
var Route = Router.Route;

var routes = [
  <Route name="home" path="/" handler={require('./components/home')} />
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
