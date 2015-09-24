'use strict';
import Flux from 'flummox';
import FluxComponent from 'flummox/component';
import React from 'react';
import _ from 'lodash';
import classNames from 'classnames';

import toString from '../utils/toString';
import { prompt } from '../utils/alert';


class UnitProperties extends React.Component {

    render() {
        var unit = this.props.unit;
        var upgradeableTo = this.props.upgradeableTo;

        return (
            <div className="pmbb-body">
                <div className="pmbb-view">
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-label m-r-5"/> Type</dt>
                        <dd>{unit.type.name}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-upload m-r-5"/> Upgrade to</dt>
                        <dd>{_.pluck(upgradeableTo, 'name').join(', ')}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-fire m-r-5"/> Attack</dt>
                        <dd>{unit.attack}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-shield-check m-r-5"/> Defence</dt>
                        <dd>{unit.defence}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-alarm m-r-5"/> Train time</dt>
                        <dd>{toString(unit.train_time, 'time')}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-money m-r-5"/> Money</dt>
                        <dd>{toString(unit.cost_money)}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-accounts m-r-5"/> Population</dt>
                        <dd>{toString(unit.cost_population)}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-widgets m-r-5"/> Iron</dt>
                        <dd>{toString(unit.cost_iron)}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-view-module m-r-5"/> Stone</dt>
                        <dd>{toString(unit.cost_stone)}</dd>
                    </dl>
                    <dl className="dl-horizontal">
                        <dt><i className="zmdi zmdi-view-headline m-r-5"/> Wood</dt>
                        <dd>{toString(unit.cost_wood)}</dd>
                    </dl>
                </div>
            </div>
        );
    }
}

UnitProperties.propTypes = {
    unit: React.PropTypes.object.isRequired,
    upgradeableTo: React.PropTypes.array
};


class Unit extends React.Component {

    render() {
        var cityUnit = this.props.cityUnit;
        var unit = this.props.unit;
        var upgradeableTo = this.props.upgradeableTo;

        return (
            <div className={classNames('col-sm-4', 'unit', unit.type.name)}>
                <div className="card">
                    <div className="card-header m-b-20">
                        <h2>
                            {_.capitalize(unit.name)}
                            <span className="pull-right">{cityUnit.number || ''}</span>
                        </h2>
                        <button onClick={this.onTrainClick.bind(this)}
                            className="btn bgm-lightgreen btn-float waves-effect waves-effect waves-circle waves-float">
                            <i className="zmdi zmdi-plus"/>
                        </button>
                    </div>

                    <div className="card-body card-padding">
                        <div className="pmb-block">
                            <UnitProperties
                                unit={unit}
                                upgradeableTo={upgradeableTo}
                                />
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    train() {
        // this.props.flux.getActions('cityActions').build(this.props.building.id).catch(showErrors);
    }

    onTrainClick() {
        var name = _.capitalize(this.props.unit.name);

        prompt({
            title: `Do you wish to train ${name}?`,
            confirmButtonText: 'Yes, train them!'
        }, this.train.bind(this));
    }
}

Unit.propTypes = {
    cityUnit: React.PropTypes.object.isRequired,
    flux: React.PropTypes.instanceOf(Flux).isRequired,
    unit: React.PropTypes.object.isRequired,
    upgradeableTo: React.PropTypes.array
};


class Units extends React.Component {

    render() {
        var units = this.props.units;
        var city = this.props.city;
        var content = 'Loading...';

        if (units && city) {
            var items = _.map(units, (unit) => {
                var cityUnit = city.units[unit.id];
                var upgradeableTo = _.map(unit.upgradeable_to, function(unitId) {
                    return units[unitId];
                });

                return (
                    <Unit key={unit.id}
                        unit={unit}
                        cityUnit={cityUnit}
                        upgradeableTo={upgradeableTo}
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

Units.propTypes = {
    units: React.PropTypes.object,
    city: React.PropTypes.object,
    flux: React.PropTypes.instanceOf(Flux).isRequired
};

export default class FluxUnits extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                unitsStore: store => ({
                    units: store.getUnits()
                }),
                cityStore: store => ({
                    city: store.getCity()
                })
            }}>
                <Units {...this.props}/>
            </FluxComponent>
        );
    }

}
