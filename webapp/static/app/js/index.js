import {Rpc} from "./rpc";

var rpc = new Rpc('ws://127.0.0.1:9000');

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

window.rpc = rpc;
