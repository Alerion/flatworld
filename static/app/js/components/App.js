import React from 'react';
import {RouteHandler} from 'react-router';
import WorldStats from './WorldStats';

export default React.createClass({
    render() {
        return (
            <div className="container">
                <WorldStats/>
                <RouteHandler/>
            </div>
        );
    }
});
