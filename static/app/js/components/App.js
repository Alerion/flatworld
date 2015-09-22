'use strict';
import React from 'react';
import { RouteHandler } from 'react-router';

import Header from './Header';
import Sidebar from './Sidebar';


export default React.createClass({
    render() {
        return (
            <section id="main">
                <Header/>
                <Sidebar/>
                <section id="content">
                    <div className="container">
                        <RouteHandler {...this.props} />
                    </div>
                </section>
            </section>
        );
    }
});
