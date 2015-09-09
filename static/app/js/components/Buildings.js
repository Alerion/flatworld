import FluxComponent from 'flummox/component';
import React from 'react';
import {showErrors} from '../utils/notify';
import {confirm} from '../utils/alert';
import {capitalize} from 'lodash/string';


class Building extends React.Component {

}


class Buildings extends React.Component {

    onBuildClick(buildingId) {
        var building = this.props.buildings.get(String(buildingId));
        var name = capitalize(building.get('name'));

        confirm({
            title: `Do you wish to build ${name}?`,
            confirmButtonText: 'Yes, build it!'
        }, this.build.bind(this, buildingId));
    }

    componentDidUpdate() {
        $(React.findDOMNode(this.refs.buildings)).find('.easy-pie').easyPieChart({
            trackColor: 'rgba(255,255,255,0.3)',
            scaleColor: false,
            barColor: 'rgba(255,255,255,0.8)',
            lineWidth: 5,
            lineCap: 'butt',
            size: 50,
            animate: false
        });
    }

    render() {
        var buildings = this.props.buildings;
        var city = this.props.city;
        var content;

        if (buildings && city) {
            let items = [];

            for (let item of buildings.values()) {
                let cityBuilding = city.get('buildings').get(String(item.get('id')));

                let buildButton;
                if (cityBuilding.get('in_progress')) {
                    // FIXME: Add timer
                    buildButton = (
                        <div className="bgm-blue btn-float">
                            <div className="easy-pie main-pie" data-percent="89">
                                <div className="percent">{cityBuilding.get('build_progress')}s</div>
                            </div>
                        </div>
                    )
                } else {
                    buildButton = (
                        <button onClick={this.onBuildClick.bind(this, item.get('id'))} className="btn bgm-blue btn-float waves-effect waves-effect waves-circle waves-float">
                            <i className="zmdi zmdi-plus"></i>
                        </button>
                    )
                }

                items.push(
                    <div key={item.get('id')} className="col-sm-4">
                        <div className="card building">
                            <div className="card-header bgm-indigo m-b-20">
                                <h2>
                                    {capitalize(item.get('name'))} [{cityBuilding.get('level')}]
                                    <small>{item.get('description')}</small>
                                </h2>

                                {buildButton}
                            </div>

                            <div className="card-body card-padding">
                                <div className="pmb-block">
                                    <div className="pmbb-body">
                                        <div className="pmbb-view">
                                            <dl className="dl-horizontal">
                                                <dt><i className="zmdi zmdi-alarm m-r-5"></i> Сonstruction time</dt>
                                                <dd>{item.get('build_time')} seconds</dd>
                                            </dl>
                                            <dl className="dl-horizontal">
                                                <dt><i className="zmdi zmdi-money m-r-5"></i> Money</dt>
                                                <dd>{item.get('cost_money')}</dd>
                                            </dl>
                                            <dl className="dl-horizontal">
                                                <dt><i className="zmdi zmdi-accounts m-r-5"></i> Population</dt>
                                                <dd>{item.get('cost_population')}</dd>
                                            </dl>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
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
            <div ref="buildings">
                <div className="block-header">
                    <h2>Building</h2>
                </div>

                {content}
            </div>
        );
    }

    build(buildingId) {
        this.props.flux.getActions('cityActions').build(buildingId).catch(showErrors);
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
