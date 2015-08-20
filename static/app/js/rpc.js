class Rpc {

    constructor(url) {
        this.url = url;
        this._socket = null;
        this._requests = new Map();
        this._observers = new Map();
        this._nextId = 1;
    }

    connect() {
        console.log('Connecting to', this.url);
        return new Promise((resolve, reject) => {
            this._socket = new WebSocket(this.url);
            this._socket.onopen = resolve;
            this._socket.onmessage = this.onMessage.bind(this);
            this._socket.onclose = this.onClose.bind(this);
            // FIXME: use reject on error
        });
    }

    onMessage(msg) {
        var response = JSON.parse(msg.data);

        if (response.type == 'rpc') {
            var promise = this._requests.get(response.id);

            if (response.event == 'success') {
                promise.resolve(response.value);
            } else {
                promise.reject(response.message);
            }
        }

        if (response.type == 'event') {
            var observers = this._observers.get(response.topic);
            if (observers) {
                for (var callback of observers) {
                    callback(response.message, response.topic);
                }
            }
        }
    }

    onClose() {
        setTimeout(this.connect.bind(this), 1000);
    }

    call(method, ...args) {
        var promise = new Promise((resolve, reject) => {
            var id = this._nextId++;

            // FIXME: clean up requests some times
            this._requests.set(id, {
                resolve: resolve,
                reject: reject
            });

            this._socket.send(JSON.stringify({
                id: id,
                method: method,
                type: 'rpc',
                args: args
            }), {binary: false});
        });

        return promise;
    }

    subscribe(topic, callback) {
        // TOD: add subscribe on server to reduce network traffic
        var observers = this._observers.get(topic);

        if ( ! observers) {
            this._observers.set(topic, [callback]);
        } else {
            observers.push(callback);
        }
    }
}

/*var rpc = new Rpc('ws://127.0.0.1:9000');

rpc.connect().then(function () {
    rpc.call('count').then(function(vaue) {
        console.log(vaue);
    });

    rpc.call('ping', 'hello').then(function(vaue) {
        console.log(vaue);
    });

    rpc.call('count').then(function(vaue) {
        console.log(vaue);
    });

    rpc.call('get_user').then(function(vaue) {
        console.log(vaue);
    });

    rpc.subscribe('events', function (message, topic) {
        console.log(topic, message);
    });

    rpc.subscribe('messages', function (message, topic) {
        console.log(topic, message);
    });
});

window.rpc = rpc;*/
