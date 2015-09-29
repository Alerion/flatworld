'use strict';
import _ from 'lodash';
import Flux from 'flummox';
import FluxComponent from 'flummox/component';
import React from 'react';
import { OverlayTrigger, Popover } from 'react-bootstrap';

import toString from '../utils/toString';
import { confirm } from '../utils/alert';
import { showErrors } from '../utils/notify';
import ProgressChart from './ProgressChart';


class BuildingTierProperties extends React.Component {

    render() {
        var buildingTier = this.props.buildingTier;

        var properties = _.map(buildingTier.properties, function(value, key) {
            const info = buildingTier.properties_description[key];

            return (
                <dl className="dl-horizontal"
                    key={key}>
                    <dt><i className="zmdi zmdi-settings m-r-5"/> {toString(key, 'key')}</dt>
                    <dd>
                        {value}
                        <OverlayTrigger overlay={<Popover id="help-{key}">{info}</Popover>}>
                            <i className="zmdi zmdi-help-outline m-l-5"/>
                        </OverlayTrigger>
                    </dd>
                </dl>
            );
        });

        return (
            <div className="pmb-block">
                <div className="pmbb-body">
                    <div className="pmbb-view">
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-alarm m-r-5"/> Сonstruction time</dt>
                            <dd>{toString(buildingTier.build_time, 'time')}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-money m-r-5"/> Money</dt>
                            <dd>{toString(buildingTier.cost_money)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-accounts m-r-5"/> Population</dt>
                            <dd>{toString(buildingTier.cost_population)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-widgets m-r-5"/> Iron</dt>
                            <dd>{toString(buildingTier.cost_iron)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-view-module m-r-5"/> Stone</dt>
                            <dd>{toString(buildingTier.cost_stone)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-view-headline m-r-5"/> Wood</dt>
                            <dd>{toString(buildingTier.cost_wood)}</dd>
                        </dl>
                        {properties}
                    </div>
                </div>
            </div>
        );
    }
}

BuildingTierProperties.propTypes = {
    buildingTier: React.PropTypes.object.isRequired
};


class Building extends React.Component {

    render() {
        var building = this.props.building;
        var cityBuilding = this.props.cityBuilding;
        var nextBuildingTier = building.tiers[cityBuilding.level + 1];

        var buildButton;
        var progressChart;
        if (cityBuilding.in_progress) {
            progressChart = (
                <ProgressChart
                    progress={cityBuilding.build_progress / nextBuildingTier.build_time * 100}
                    value={cityBuilding.build_progress}
                    />
            );
        } else if (nextBuildingTier) {
            buildButton = (
                <button onClick={this.onBuildClick.bind(this)}
                    className="btn bgm-green btn-float waves-effect waves-effect waves-circle waves-float">
                    <i className="zmdi zmdi-plus"/>
                </button>
            );
        }

        var buildingTierProperties;
        if (nextBuildingTier) {
            buildingTierProperties = <BuildingTierProperties buildingTier={nextBuildingTier} />;
        } else {
            buildingTierProperties = 'Building has max level.';
        }

        return (
            <div className="col-sm-4">
                <div className="card building">
                    <div className="card-header bgm-teal m-b-20">
                        <h2>
                            {_.capitalize(building.name)} [{nextBuildingTier ? cityBuilding.level : 'MAX'}]
                            <small>{building.description}</small>
                        </h2>
                        {progressChart}
                        {buildButton}
                    </div>

                    <div className="card-body card-padding">
                        {buildingTierProperties}
                    </div>
                </div>
            </div>
        );
    }

    build() {
        this.props.flux.getActions('cityActions').build(this.props.building.id).catch(showErrors);
    }

    onBuildClick() {
        var name = _.capitalize(this.props.building.name);

        confirm({
            title: `Do you wish to build ${name}?`,
            confirmButtonText: 'Yes, build it!'
        }, this.build.bind(this));
    }
}

Building.propTypes = {
    building: React.PropTypes.object.isRequired,
    cityBuilding: React.PropTypes.object.isRequired,
    flux: React.PropTypes.instanceOf(Flux).isRequired
};


class Buildings extends React.Component {

    render() {
        var buildings = this.props.buildings;
        var city = this.props.city;
        var content = 'Loading...';

        if (buildings && city) {
            var items = _.map(buildings, (building) => {
                var cityBuilding = city.buildings[building.id];
                return (
                    <Building key={building.id}
                        cityBuilding={cityBuilding}
                        building={building}
                        flux={this.props.flux}
                        />
                );
            });

            content = [];
            var group = [];
            items.forEach(function(item, i) {
                if (i % 3 === 0 && i !== 0) {
                    content.push(
                        <div key={content.length}
                            className="row card-group">
                            {group}
                        </div>
                    );
                    group = [];
                }
                group.push(item);
            });
            content.push(
                <div
                    key={content.length}
                    className="row card-group">
                    {group}
                </div>);
        }

        return (
            <div>
                {content}
            </div>
        );
    }
}

Buildings.propTypes = {
    buildings: React.PropTypes.object,
    city: React.PropTypes.object,
    flux: React.PropTypes.instanceOf(Flux).isRequired
};



export default class FluxBuilding extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                buildingsStore: store => ({
                    buildings: store.getBuildings()
                }),
                cityStore: store => ({
                    city: store.getCity()
                })
            }}>
                <Buildings {...this.props}/>
            </FluxComponent>
        );
    }
}
