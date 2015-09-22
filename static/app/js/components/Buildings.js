import FluxComponent from 'flummox/component';
import React from 'react';
import { OverlayTrigger, Popover } from 'react-bootstrap';

import toString from '../utils/toString';
import { capitalize, map } from 'lodash';
import { confirm } from '../utils/alert';
import { showErrors } from '../utils/notify';


class ProgressChart extends React.Component {

    componentDidMount() {
        $(React.findDOMNode(this.refs.progressChart)).easyPieChart({
            trackColor: false,
            scaleColor: false,
            barColor: 'rgba(255,255,255,0.7)',
            lineWidth: 5,
            lineCap: 'butt',
            size: 50,
            animate: false
        });
    }

    componentDidUpdate() {
        $(React.findDOMNode(this.refs.progressChart))
            .data('easyPieChart')
            .update(this.props.progress);
    }

    render() {
        return (
            <div className="bgm-green btn-float">
                <div ref="progressChart" className="easy-pie main-pie" data-percent={this.props.progress}>
                    <div className="percent">{this.props.timeLeft}</div>
                </div>
            </div>
        )
    }
}


class BuildingTierProperties extends React.Component {

    render () {
        var buildingTier = this.props.buildingTier;

        var properties = map(buildingTier.properties, function(value, key) {
            let info = buildingTier.properties_description[key];

            return (
                <dl key={key} className="dl-horizontal">
                    <dt><i className="zmdi zmdi-settings m-r-5"></i> {toString(key, 'key')}</dt>
                    <dd>
                        {value}
                        <OverlayTrigger overlay={<Popover id="help-{key}">{info}</Popover>}>
                            <i className="zmdi zmdi-help-outline m-l-5"></i>
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
                            <dt><i className="zmdi zmdi-alarm m-r-5"></i> Сonstruction time</dt>
                            <dd>{toString(buildingTier.build_time, 'time')}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-money m-r-5"></i> Money</dt>
                            <dd>{toString(buildingTier.cost_money)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-accounts m-r-5"></i> Population</dt>
                            <dd>{toString(buildingTier.cost_population)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-widgets m-r-5"></i> Iron</dt>
                            <dd>{toString(buildingTier.cost_iron)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-view-module m-r-5"></i> Stone</dt>
                            <dd>{toString(buildingTier.cost_stone)}</dd>
                        </dl>
                        <dl className="dl-horizontal">
                            <dt><i className="zmdi zmdi-view-headline m-r-5"></i> Wood</dt>
                            <dd>{toString(buildingTier.cost_wood)}</dd>
                        </dl>
                        {properties}
                    </div>
                </div>
            </div>
        );
    }
}


class Building extends React.Component {

    render() {
        var building = this.props.building;
        var cityBuilding = this.props.cityBuilding;
        var nextBuildingTier = building.tiers[cityBuilding.level + 1];

        var buildButton;
        var progressChart;
        if (cityBuilding.in_progress) {
            progressChart = <ProgressChart
                progress={cityBuilding.build_progress / nextBuildingTier.build_time * 100}
                timeLeft={cityBuilding.build_progress}
            />
        } else if (nextBuildingTier) {
            buildButton = (
                <button onClick={this.onBuildClick.bind(this)} className="btn bgm-green btn-float waves-effect waves-effect waves-circle waves-float">
                    <i className="zmdi zmdi-plus"></i>
                </button>
            )
        }

        var buildingTierProperties;
        if (nextBuildingTier) {
            buildingTierProperties = <BuildingTierProperties buildingTier={nextBuildingTier} />;
        } else {
            buildingTierProperties = 'Building has max level.'
        }

        return (
            <div className="col-sm-4">
                <div className="card building">
                    <div className="card-header bgm-teal m-b-20">
                        <h2>
                            {capitalize(building.name)} [{nextBuildingTier ? cityBuilding.level : 'MAX'}]
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
        )
    }

    build() {
        this.props.flux.getActions('cityActions').build(this.props.building.id).catch(showErrors);
    }

    onBuildClick() {
        var name = capitalize(this.props.building.name);

        confirm({
            title: `Do you wish to build ${name}?`,
            confirmButtonText: 'Yes, build it!'
        }, this.build.bind(this));
    }
}


class Buildings extends React.Component {

    render() {
        var buildings = this.props.buildings;
        var city = this.props.city;
        var content;

        if (buildings && city) {
            var items = map(buildings, (building) => {
                var cityBuilding = city.buildings[building.id];
                return <Building key={building.id} cityBuilding={cityBuilding} building={building} flux={this.props.flux} />;
            });

            var content = [];
            var group = [];
            items.forEach(function(item, i) {
                if (i % 3 === 0 && i !== 0) {
                    content.push(<div key={content.length} className="row card-group m-25">{group}</div>);
                    group = [];
                }
                group.push(item);
            }.bind(this));
            content.push(<div key={content.length} className="row card-group m-25">{group}</div>);
        } else {
            content = 'Loading...';
        }

        return (
            <div>
                <div className="block-header">
                    <h2>Building</h2>
                </div>

                {content}
            </div>
        );
    }
}

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
