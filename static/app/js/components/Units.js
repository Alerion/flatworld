import FluxComponent from 'flummox/component';
import React from 'react';

import toString from '../utils/toString';


class Units extends React.Component {

    render() {
        return (
            <div>
                <div className="block-header">
                    <h2>Units</h2>
                </div>

                Units list
            </div>
        );
    }
}

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
