'use strict';
import React from 'react';


export default class ProgressChart extends React.Component {

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
            <div className="bgm-green btn-float">
                <div className="easy-pie main-pie"
                    data-percent={this.props.progress}
                    ref="progressChart">
                    <div className="percent">{this.props.value}</div>
                </div>
            </div>
        );
    }
}

ProgressChart.propTypes = {
    progress: React.PropTypes.number.isRequired,
    value: React.PropTypes.any.isRequired
};
