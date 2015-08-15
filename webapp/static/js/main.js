function onchallenge (session, method, extra) {
    var KEY = 'user';
    //console.log("onchallenge", method, extra);
    if (method === "wampcra") {
        console.log("onchallenge: authenticating via '" + method + "' and challenge '" + extra.challenge + "'");
        return autobahn.auth_cra.sign(KEY, extra.challenge);
    } else {
        throw "don't know how to authenticate using '" + method + "'";
    }
}
// TODO: add failed auth handler
var connection = new autobahn.Connection({
    url: 'ws://127.0.0.1:8080/ws',
    realm: 'frontend',
    max_retries: 3,
    authmethods: ["wampcra"],
    authid: "user",
    onchallenge: onchallenge
});


connection.onopen = function (session) {

    window.call = function call(command) {
        session.call(command).then(function(result) {
            console.log(result);
        });
    };
};

connection.oncsole = function (reason, details) {
    console.log(reason, details);
};

connection.open();
