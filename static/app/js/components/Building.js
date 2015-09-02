import FluxComponent from 'flummox/component';
import React from 'react';
import {Link} from 'react-router';


class Building extends React.Component {

    render() {
        var buildings = this.props.buildings;
        var content;

        if (buildings) {
            content = (
                <div className="pmb-block">
                    <div className="pmbb-body">
                        <div className="pmbb-view">
                            {buildings.map(function (item) {
                                return (
                                    <dl key={item.get('id')} className="dl-horizontal">
                                        <dt>{item.get('name')}</dt>
                                        <dd>1</dd>
                                    </dl>);
                            })}
                        </div>
                    </div>
                </div>
            );
        } else {
            content = 'Loading...';
        }

        return (
            <div className="card">
                <div className="card-header">
                    <h2>Buildings</h2>
                    <Link to="world" params={{worldId: this.props.worldId}}>Map</Link>
                </div>

                <div className="card-body card-padding">
                    {content}
                </div>
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
