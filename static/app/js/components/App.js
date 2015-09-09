import React from 'react';
import {RouteHandler} from 'react-router';
import WorldStats from './WorldStats';
import CitiesStats from './CitiesStats';
import Header from './Header';


export default React.createClass({
    render() {
        return (
            <section id="main">
                <Header/>
                <section id="content">
                    <div className="container">
                        <RouteHandler {...this.props} />
                    </div>
                </section>
            </section>
        );
    }
});
