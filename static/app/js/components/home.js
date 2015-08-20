var React = require('react');
var Marty = require('marty');

class Home extends React.Component {

    constructor(props, context) {
        super(props, context);
    }

    render() {
        return (
            <div className="home">Hello world!</div>
        );
    }
}

module.exports = Marty.createContainer(Home, {});
