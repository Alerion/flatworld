import React from 'react';
import { uniqueId } from 'lodash';
import { Grid, Row, Col } from 'react-bootstrap';


class Slider extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            active: true,
            value: 0
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
            start: this.state.value,
            step: 10,
            range: {
                'min': -200,
                'max': 200,
            },
            pips: pips,
            format: {
                to: function ( value ) {
                    return value;
                },
                from: function ( value ) {
                    return value;
                }
            }
        });

        slider.noUiSlider.on('update', (values, handle) => {
            this.setState({
                active: true,
                value: values[0]
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
                        <strong className="text-muted">{this.state.value}</strong>
                    </Col>
                </Row>
            </Grid>
        );
    }

    onChageActive() {
        this.setState({active: ! this.state.active});
    }
}


class ActiveRange extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            start: -100,
            end: 0
        };
    }

    componentDidMount() {
        var slider = React.findDOMNode(this.refs.slider);

        noUiSlider.create(slider, {
            start: [this.state.start, this.state.end],
            step: 1,
            connect: true,
            behaviour: 'tap-drag-fixed',
            range: {
                'min': -200,
                'max': 200,
            },
            format: {
                to: function ( value ) {
                    return value;
                },
                from: function ( value ) {
                    return value;
                }
            }
        });

        slider.noUiSlider.on('update', (values, handle) => {
            if (handle) {
                this.setState({
                    start: values[handle]
                });
            } else {
                this.setState({
                    end: values[handle]
                });
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
                        <strong className="text-muted">{this.state.end} : {this.state.start}</strong>
                    </Col>
                </Row>
            </Grid>
        );
    }
}


export default class QuestDemo extends React.Component {

    render() {
        return (
            <div className="card">
                <div className="card-header">
                    <h2>Quests demo</h2>
                </div>

                <div className="card-body card-padding">
                    <p className="f-500 c-black m-b-20">Output Value with tap and drag</p>

                    <div className="m-b-20 clearfix">
                        <Slider color="red"/>
                        <Slider color="amber"/>
                        <Slider color="green"/>
                        <Slider color="cyan"/>
                        <Slider color="blue" pips={true}/>
                        <ActiveRange/>
                    </div>
                </div>
            </div>
        )
    }
}
