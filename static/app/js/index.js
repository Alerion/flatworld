var React = require('react');
var Router = require('./router');

window.React = React; // For React Developer Tools


Router.run(function (Handler, state) {
    React.render(<Handler {...state.params} />, document.getElementById('app'));
});
