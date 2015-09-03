import FluxComponent from 'flummox/component';
import React from 'react';

import Application from './Application'
import router from './router';
import Rpc from './Rpc'

window.React = React; // For React Developer Tools


async function main() {
    const url = `ws://${CONFIG.FRONTEND_ADDR}:${CONFIG.FRONTEND_PORT}?world_id=${CONFIG.WORLD_ID}`;
    console.log('Connectiong...', url);
    const rpc = new Rpc(url);
    await rpc.connect();
    console.log('Connected');

    // For debugging in console
    window.rpc = rpc;

    const flux = new Application(rpc);

    router.run(function (Handler, state) {
        React.render(
            <FluxComponent flux={flux}>
                <Handler {...state.params} />
            </FluxComponent>,
            document.getElementById('content')
        );
    });
}

main();
