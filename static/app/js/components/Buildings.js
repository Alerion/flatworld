import FluxComponent from 'flummox/component';
import React from 'react';
import {showErrors} from '../utils/notify';
import {confirm} from '../utils/alert';
import {capitalize} from 'lodash/string';


class Building extends React.Component {

    constructor(props) {
        super();
        this.state = this._getProgressState(props);
        this.timer = null;
    }

    componentWillReceiveProps(nextProps) {
        this.setState(this._getProgressState(nextProps));
    }

    componentDidMount() {
        this._initChart();
        this.timer = setInterval(this._tick.bind(this), 1000);
    }

    componentDidUpdate() {
        this._initChart();
    }

    componentWillUnmount() {
        clearInterval(this.timer);
    }

    render() {
        var building = this.props.building;
        var cityBuilding = this.props.cityBuilding;

        var buildButton;
        var progressChart;
        if (cityBuilding.get('in_progress')) {
            // FIXME: Add timer
            progressChart = (
                <div className="bgm-blue btn-float">
                    <div ref="progressChart" className="easy-pie main-pie" data-percent={this.state.progressInPerc}>
                        <div className="percent">{this.state.progressInSec}</div>
                    </div>
                </div>
            )
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

    _tick() {
        // FIXME: Use world speed
        if (this.state.progressInSec && this.state.progressInSec > 0) {
            this.setState({
                progressInSec: this.state.progressInSec - 1,
                progressInPerc: (this.state.progressInSec - 1) / this.props.building.get('build_time') * 100
            });
        }
    }

    _initChart() {
        if (this.refs.progressChart) {
            $(React.findDOMNode(this.refs.progressChart)).easyPieChart({
                trackColor: false,
                scaleColor: false,
                barColor: 'rgba(255,255,255,0.7)',
                lineWidth: 5,
                lineCap: 'butt',
                size: 50,
                animate: false
            }).data('easyPieChart').update(this.state.progressInPerc);
        }
    }

    _getProgressState(props) {
        if (props.cityBuilding.get('in_progress')) {
            var progressInSec = props.cityBuilding.get('build_progress')
            return {
                progressInSec: progressInSec,
                progressInPerc: progressInSec / props.building.get('build_time') * 100
            }
        }
        return {}
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
