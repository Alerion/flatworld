export class Rpc {
    constructor(url) {
        this.url = url;
        this._socket = null;
        this._requests = new Map();
        this._nextId = 1;
    }

    connect() {
        return new Promise((resolve, reject) => {
            this._socket = new WebSocket(this.url);
            this._socket.onopen = resolve;
            this._socket.onmessage = this.onMessage.bind(this);
            this._socket.onclose = this.onClose.bind(this);
        });
    }

    onMessage(msg) {
        var response = JSON.parse(msg.data);

        if (response.type == 'rpc') {
            let promise = this._requests.get(response.id);

            if (response.event == 'success') {
                promise.resolve(response.value);
            } else {
                promise.reject(response.message);
            }
        }
    }

    onClose() {
        console.log(arguments);
    }

    call(method, ...args) {
        let promise = new Promise((resolve, reject) => {
            let id = this._nextId++;

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

}
