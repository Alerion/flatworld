'use strict';
import FluxComponent from 'flummox/component';
import React from 'react';

import toString from '../utils/toString';

// FIXME: use new World object
class CitiesStats extends React.Component {

    render() {
        var world = this.props.world;
        var content;

        if (world) {
            var rows = [];

            for (const region of world.get('regions').values()) {
                rows.push(
                    <tr key={region.get('id')}><th>{region.get('name')}</th></tr>
                );

                for (const city of region.get('cities').values()) {
                    rows.push(
                        <tr key={city.get('id')}>
                            <td>{city.get('name')}</td>
                            <td>{toString(city.get('stats').get('population'))}</td>
                            <td>{toString(city.get('stats').get('money'))}</td>
                        </tr>
                    );
                }
            }
            content = (
                <div className="table-responsive">
                    <table className="table table-condensed">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Population</th>
                                <th>Money</th>
                            </tr>
                        </thead>

                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                </div>
            );
        } else {
            content = 'Loading...';
        }

        return (
            <div className="card">
                <div className="card-header">
                    <h2>Cities</h2>
                </div>

                <div className="card-body">
                    {content}
                </div>
            </div>
        );
    }
}

CitiesStats.propTypes = {
    world: React.PropTypes.object
};


export default class FluxWorldStats extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                worldStore: store => ({
                    world: store.getWorld()
                })
            }}>
                <CitiesStats {...this.props}/>
            </FluxComponent>
        );
    }

}
