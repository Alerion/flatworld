import React from 'react';
import { uniqueId, max, min, filter } from 'lodash';
import { Grid, Row, Col } from 'react-bootstrap';


class Slider extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            active: true
        };
    }

    componentDidMount() {
        var slider = React.findDOMNode(this.refs.slider);
        var pips = null;

        if (this.props.pips) {
            pips = {
                mode: 'values',
                values: [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100]
            }
        }

        noUiSlider.create(slider, {
            start: this.props.value,
            step: 5,
            range: {
                'min': -200,
                'max': 200,
            },
            format: {
                to: function (value) {
                    return value;
                },
                from: function (value) {
                    return Number(value);
                }
            },
            pips: pips
        });

        slider.noUiSlider.on('update', (values, handle) => {
            this.props.onChange(values[handle]);
            this.setState({
                active: true
            });
        });
    }

    render() {
        var id = uniqueId('slider_');
        return (
            <Grid className="m-0 m-t-10">
                <Row className="m-0">
                    <Col xs={12} md={1}>
                        <div className="toggle-switch">
                            <input id={id} onChange={this.onChageActive.bind(this)} checked={this.state.active} type="checkbox" hidden="hidden"/>
                            <label htmlFor={id} className="ts-helper"/>
                        </div>
                    </Col>
                    <Col xs={12} md={10}>
                        <div ref="slider" className="input-slider-values m-b-15" data-is-color={this.props.color}></div>
                    </Col>
                    <Col xs={12} md={1} style={{marginTop: -9}}>
                        <strong className="text-muted">{this.props.value}</strong>
                    </Col>
                </Row>
            </Grid>
        );
    }

    onChageActive() {
        if (this.state.active) {
            this.setState({active: false});
            this.props.onChange(null);
        } else {
            this.setState({active: true});
            this.props.onChange(React.findDOMNode(this.refs.slider).noUiSlider.get(0));
        }
    }
}


class ActiveRange extends React.Component {

    componentDidMount() {
        var slider = React.findDOMNode(this.refs.slider);

        noUiSlider.create(slider, {
            start: [this.props.start, this.props.end],
            step: 5,
            connect: true,
            behaviour: 'tap-drag-fixed',
            range: {
                'min': -200,
                'max': 200,
            },
            format: {
                to: function (value) {
                    return value;
                },
                from: function (value) {
                    return Number(value);
                }
            }
        });

        slider.noUiSlider.on('update', (values, handle) => {
            if (handle) {
                this.props.onEndChange(values[handle]);
            } else {
                this.props.onStartChange(values[handle]);
            }
        });
    }

    render() {
        return (
            <Grid className="m-0 m-t-25">
                <Row className="m-0 m-t-10">
                    <Col xs={12} md={1}>&nbsp;</Col>
                    <Col xs={12} md={10}>
                        <div ref="slider" className="input-slider-values m-b-15" data-is-color={this.props.color}></div>
                    </Col>
                    <Col xs={12} md={1} style={{marginTop: -9}}>
                        <strong className="text-muted">{this.props.start} : {this.props.end}</strong>
                    </Col>
                </Row>
            </Grid>
        );
    }
}


class Chart extends React.Component {

    constructor(props, context) {
        super(props, context);
        this._plot = null;
    }

    componentDidMount() {
        this._plot = $.plot(React.findDOMNode(this.refs.chart), this.getData(), {
            series: {
                pie: {
                    show: true,
                    stroke: {
                        width: 2,
                    },
                },
            },
            legend: {
                container: '.flc-pie',
                backgroundOpacity: 0.5,
                noColumns: 0,
                backgroundColor: "white",
                lineWidth: 0
            }
        });
    }

    componentDidUpdate() {
        this._plot.setData(this.getData());
        this._plot.draw();
    }

    render() {
        return (
            <div className="m-b-20 clearfix">
                <div ref="chart" style={{height: 300}}></div>
                <div className="flc-pie hidden-xs"></div>
            </div>
        );
    }

    getData() {
        return [
            {data: this.props.fail2, color: '#f44336', label: 'fail2'},
            {data: this.props.fail1, color: '#FF5722', label: 'fail1'},
            {data: this.props.fail, color: '#FFC107', label: 'fail'},
            {data: this.props.win, color: '#4caf50', label: 'win'},
            {data: this.props.win1, color: '#00bcd4', label: 'win1'},
            {data: this.props.win2, color: '#2196f3', label: 'win2'},
        ]
    }
}


export default class QuestDemo extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            fail2: -75,
            fail1: -50,
            fail: 0,
            win: 50,
            win1: 75,
            start: -100,
            end: 0
        };
    }

    onValueChange(name, value) {
        this.setState({[name]: value});
    }

    getProbabilities() {
        var items = ['fail2', 'fail1', 'fail', 'win', 'win1', 'win2'];
        var ranges = {};
        var last = null;

        for (let item of items) {
            let start = null;
            if (last !== null) {
                start = last[1];
            }
            let end = this.state[item];
            if (end === undefined) {
                end = null;
            }
            last = [start, end];
            ranges[item] = last;
        }

        var data = {}

        for (let item of items) {
            let start = ranges[item][0];
            let end = ranges[item][1];

            if (start === null && end === null) {
                data[item] = 0;
                continue;
            } else if (start === null) {
                start = -200;
            } else if (end === null) {
                end = 200;
            }

            if (start > this.state.end || end < this.state.start) {
               data[item] = 0;
            } else {
                start = max([start, this.state.start]);
                end = min([end, this.state.end]);
                data[item] = end - start;
            }
        }

        return data;
    }

    render() {
        return (
            <div className="card">
                <div className="card-header">
                    <h2>Quests demo</h2>
                </div>

                <div className="card-body card-padding">
                    <p className="f-500 c-black m-b-20">Change Output Value with tap and drag</p>

                    <div className="m-b-20 clearfix">
                        <Slider color="red" value={this.state.fail2} onChange={this.onValueChange.bind(this, 'fail2')}/>
                        <Slider color="amber" value={this.state.fail1} onChange={this.onValueChange.bind(this, 'fail1')}/>
                        <Slider color="green" value={this.state.fail} onChange={this.onValueChange.bind(this, 'fail')}/>
                        <Slider color="cyan" value={this.state.win} onChange={this.onValueChange.bind(this, 'win')}/>
                        <Slider color="blue" value={this.state.win1} onChange={this.onValueChange.bind(this, 'win1')} pips={true}/>
                        <ActiveRange
                            start={this.state.start}
                            end={this.state.end}
                            onStartChange={this.onValueChange.bind(this, 'start')}
                            onEndChange={this.onValueChange.bind(this, 'end')}
                        />
                    </div>

                    <Chart {...this.getProbabilities()}/>
                </div>
            </div>
        )
    }
}
