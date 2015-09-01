import React from 'react';
import {RouteHandler} from 'react-router';
import WorldStats from './WorldStats';
import CitiesStats from './CitiesStats';


export default React.createClass({
    render() {
        return (
            <div className="container">
                <RouteHandler/>
                <WorldStats/>
                <CitiesStats/>
            </div>
        );
    }
});
