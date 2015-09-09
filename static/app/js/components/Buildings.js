import FluxComponent from 'flummox/component';
import React from 'react';
import {showErrors} from '../utils/notify';
import {confirm} from '../utils/alert';
import {capitalize} from 'lodash/string';


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
            <div className="bgm-blue btn-float">
                <div ref="progressChart" className="easy-pie main-pie" data-percent={this.props.progress}>
                    <div className="percent">{this.props.timeLeft}</div>
                </div>
            </div>
        )
    }
}


class Building extends React.Component {

    render() {
        var building = this.props.building;
        var cityBuilding = this.props.cityBuilding;

        var buildButton;
        var progressChart;
        if (cityBuilding.get('in_progress')) {
            progressChart = <ProgressChart
                progress={cityBuilding.get('build_progress') / building.get('build_time') * 100}
                timeLeft={cityBuilding.get('build_progress')}
            />
        } else {
            buildButton = (
                <button onClick={this.onBuildClick.bind(this)} className="btn bgm-blue btn-float waves-effect waves-effect waves-circle waves-float">
                    <i className="zmdi zmdi-plus"></i>
                </button>
            )
        }

        return (
            <div className="col-sm-4">
                <div className="card building">
                    <div className="card-header bgm-indigo m-b-20">
                        <h2>
                            {capitalize(building.get('name'))} [{cityBuilding.get('level')}]
                            <small>{building.get('description')}</small>
                        </h2>
                        {progressChart}
                        {buildButton}
                    </div>

                    <div className="card-body card-padding">
                        <div className="pmb-block">
                            <div className="pmbb-body">
                                <div className="pmbb-view">
                                    <dl className="dl-horizontal">
                                        <dt><i className="zmdi zmdi-alarm m-r-5"></i> Сonstruction time</dt>
                                        <dd>{building.get('build_time')} seconds</dd>
                                    </dl>
                                    <dl className="dl-horizontal">
                                        <dt><i className="zmdi zmdi-money m-r-5"></i> Money</dt>
                                        <dd>{building.get('cost_money')}</dd>
                                    </dl>
                                    <dl className="dl-horizontal">
                                        <dt><i className="zmdi zmdi-accounts m-r-5"></i> Population</dt>
                                        <dd>{building.get('cost_population')}</dd>
                                    </dl>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    build() {
        this.props.flux.getActions('cityActions').build(this.props.building.get('id')).catch(showErrors);
    }

    onBuildClick() {
        var name = capitalize(this.props.building.get('name'));

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
            let items = [];

            for (let building of buildings.values()) {
                let cityBuilding = city.get('buildings').get(String(building.get('id')));
                items.push(<Building key={building.get('id')} cityBuilding={cityBuilding} building={building} flux={this.props.flux} />);
            }

            var content = [];
            var group = [];
            items.forEach(function(item, i) {
                if (i % 3 === 0 && i !== 0) {
                    content.push(<div key={content.length} className="row">{group}</div>);
                    group = [];
                }
                group.push(item);
            }.bind(this));
            content.push(<div key={content.length} className="row">{group}</div>);
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
