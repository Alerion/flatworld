'use strict';
import FluxComponent from 'flummox/component';
import React from 'react';
import { OverlayTrigger, Popover } from 'react-bootstrap';

import toString from '../utils/toString';


class Header extends React.Component {

    render() {
        var city = this.props.city;

        var resources;
        if (city) {
            resources = (
                <li>
                    <ul className="city-resources">
                        <OverlayTrigger placement='left'
                            overlay={<Popover id="resources-population">
                                    <strong>Population</strong><br/>
                                    growth: {toString(city.stats.population_growth, 'int')}
                                </Popover>}>
                            <li>
                                <i className="zmdi zmdi-accounts zmdi-hc-lg"/>
                                &nbsp;{toString(city.stats.population)}
                            </li>
                        </OverlayTrigger>
                        <OverlayTrigger placement='left'
                            overlay={<Popover id="resources-money">
                                    <strong>Money</strong><br/>
                                    tax {toString(city.stats.tax, 'float')}, income: {toString(city.stats.pasive_income)}
                                </Popover>}>
                            <li>
                                <i className="zmdi zmdi-money zmdi-hc-lg"/>
                                &nbsp;{toString(city.stats.money, 'int')}
                            </li>
                        </OverlayTrigger>
                        <OverlayTrigger placement='left'
                            overlay={<Popover id="resources-iron">
                                    <strong>Iron</strong><br/>
                                    income: {toString(city.stats.iron_income)}
                                </Popover>}>
                            <li>
                                <i className="zmdi zmdi-widgets zmdi-hc-lg"/>
                                &nbsp;{toString(city.stats.iron, 'int')}
                            </li>
                        </OverlayTrigger>
                        <OverlayTrigger placement='left'
                            overlay={<Popover id="resources-stone">
                                    <strong>Stone</strong><br/>
                                    income: {toString(city.stats.stone_income)}
                                </Popover>}>
                            <li>
                                <i className="zmdi zmdi-view-module zmdi-hc-lg"/>
                                &nbsp;{toString(city.stats.stone, 'int')}
                            </li>
                        </OverlayTrigger>
                        <OverlayTrigger placement='left'
                            overlay={<Popover id="resources-wood">
                                    <strong>Wood</strong><br/>
                                    income: {toString(city.stats.wood_income)}
                                </Popover>}>
                            <li>
                                <i className="zmdi zmdi-view-headline zmdi-hc-lg"/>
                                &nbsp;{toString(city.stats.wood, 'int')}
                            </li>
                        </OverlayTrigger>
                    </ul>
                </li>
            );
        }

        return (
            <header id="header">
                <ul className="header-inner">
                    <li id="menu-trigger"
                        data-trigger="#sidebar">
                        <div className="line-wrap">
                            <div className="line top"></div>
                            <div className="line center"></div>
                            <div className="line bottom"></div>
                        </div>
                    </li>

                    <li className="logo hidden-xs">
                        <a href="/">Flat World</a>
                    </li>

                    <li className="pull-right">
                        <ul className="top-menu">
                            {resources}
                        </ul>
                    </li>
                </ul>
            </header>
        );
    }
}

Header.propTypes = {
    city: React.PropTypes.object
};


export default class FluxHeader extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                cityStore: store => ({
                    city: store.getCity()
                })
            }}>
                <Header {...this.props}/>
            </FluxComponent>
        );
    }

}
