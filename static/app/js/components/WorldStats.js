import FluxComponent from 'flummox/component';
import React from 'react';


class WorldStats extends React.Component {

    render() {
        var world = this.props.world;
        var content;

        if (world) {
            content = (
                <div className="pmb-block">
                    <div className="pmbb-body">
                        <div className="pmbb-view">
                            <dl className="dl-horizontal">
                                <dt>Total population</dt>
                                <dd>{world.totalPopulation({verbose: true})}</dd>
                            </dl>
                            <dl className="dl-horizontal">
                                <dt>Total money</dt>
                                <dd>{world.totalMoney({verbose: true})}</dd>
                            </dl>
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
                    <h2>World statistic</h2>
                    <small>Some general information about the world.</small>
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
                worldStore: store => ({
                    world: store.getWorld()
                })
            }}>
                <WorldStats/>
            </FluxComponent>
        );
    }

}
