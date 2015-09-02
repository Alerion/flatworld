import FluxComponent from 'flummox/component';
import React from 'react';


class CitiesStats extends React.Component {

    render() {
        var world = this.props.world;
        var content;

        if (world) {
            var rows = [];

            for (let region of world.get('regions').values()) {
                rows.push(
                    <tr key={region.get('id')}><th>{region.get('name')}</th></tr>
                );

                for (let city of region.get('cities').values()) {
                    rows.push(
                        <tr key={city.get('id')}>
                            <td>{city.get('name')}</td>
                            <td>{city.get('stats').get('population')}</td>
                            <td>{city.get('stats').get('money')}</td>
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

export default class FluxWorldStats extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                worldStore: store => ({
                    world: store.getWorld()
                })
            }}>
                <CitiesStats/>
            </FluxComponent>
        );
    }

}
