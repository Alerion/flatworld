import FluxComponent from 'flummox/component';
import React from 'react';
import {showErrors} from '../utils/notify';
import {confirm} from '../utils/alert';
import {capitalize} from 'lodash/string';


class Building extends React.Component {

    onBuildClick(buildingId) {
        var building = this.props.buildings.get(String(buildingId));
        var name = capitalize(building.get('name'));

        confirm({
            title: `Do you wish to build ${name}?`,
            confirmButtonText: 'Yes, build it!'
        }, this.build.bind(this, buildingId));
    }

    build(buildingId) {
        this.props.flux.getActions('buildingsActions').build(buildingId).catch(showErrors);
    }

    render() {
        var buildings = this.props.buildings;
        var content;

        if (buildings) {
            let items = [];

            for (let item of buildings.values()) {
                items.push(
                    <div key={item.get('id')} className="col-sm-4">
                        <div className="card building">
                            <div className="card-header bgm-indigo m-b-20">
                                <h2>
                                    {capitalize(item.get('name'))}
                                    <small>{item.get('description')}</small>
                                </h2>

                                <button onClick={this.onBuildClick.bind(this, item.get('id'))} className="btn bgm-blue btn-float waves-effect waves-effect waves-circle waves-float">
                                    <i className="zmdi zmdi-plus"></i>
                                </button>
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
            <div>
                <div className="block-header">
                    <h2>Building</h2>
                </div>

                {content}
            </div>
        );
    }
}

export default class FluxWorldStats extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                buildingsStore: store => ({
                    buildings: store.getBuildings()
                })
            }}>
                <Building {...this.props}/>
            </FluxComponent>
        );
    }

}
