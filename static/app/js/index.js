var React = require('react');
var Marty = require('marty');

var Application = require('./application');
var Router = require('./router');

window.React = React; // For React Developer Tools
window.Marty = Marty; // For Marty Developer Tools

var app = new Application();

Router.run(function (Handler, state) {
    React.render((
        <Marty.ApplicationContainer app={app}>
            <Handler {...state.params} />
        </Marty.ApplicationContainer>
    ), document.getElementById('app'));
});
