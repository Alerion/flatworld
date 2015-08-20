var Marty = require('marty');

class Application extends Marty.Application {
    constructor(options) {
        super(options);

        this.router = require('./router');
    }
}

module.exports = Application;
