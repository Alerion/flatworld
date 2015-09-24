'use strict';
import FluxComponent from 'flummox/component';
import React from 'react';
import _ from 'lodash';

import toString from '../utils/toString';


class Quest extends React.Component {

    render() {
        var quest = this.props.quest;

        var required = '';
        if (quest.required) {
            required = (
                <li>
                    <i className="zmdi zmdi-flash m-r-5"/>Required
                </li>
            );
        }

        var repeatable = '';
        if (quest.repeatable) {
            repeatable = (
                <li>
                    <i className="zmdi zmdi-refresh-alt m-r-5"/>Repeatable
                </li>
            );
        }

        var worldEvent = '';
        var regionsEvent = '';
        if (_.isEmpty(quest.regions) && _.isEmpty(quest.cities)) {
            worldEvent = (
                <li>
                    <i className="zmdi zmdi-globe m-r-5"/>World event
                </li>
            );
        } else if (! _.isEmpty(quest.regions)) {
            regionsEvent = (
                <li>
                    <i className="zmdi zmdi-wallpaper m-r-5"/>Regions event
                </li>
            );
        }

        var lastTill = '';
        if (quest.last_till) {
            lastTill = (
                <li>
                    <i className="zmdi zmdi-alarm m-r-5"/>
                    Ends {toString(quest.last_till, 'fromDate')}
                </li>
            );
        }

        console.log(quest);
        return (
            <div className="lv-item media quest">
                <div className="buttons pull-left">
                    <button onClick={this.onJoinClick.bind(this)}
                        className="btn bgm-green btn-float waves-effect waves-effect waves-circle waves-float">
                        <i className="zmdi zmdi-directions-run"/>
                    </button>
                </div>
                <div className="media-body">
                    <div className="lv-title">{quest.name}</div>
                    <small className="lv-small">{quest.description}</small>
                    <ul className="lv-attrs">
                        <li>
                            <i className="zmdi zmdi-hourglass-outline m-r-5"/>{toString(quest.duration, 'time')}
                        </li>
                        {required}
                        {repeatable}
                        {lastTill}
                        {worldEvent}
                        {regionsEvent}
                    </ul>
                </div>
            </div>
        );
    }

    onJoinClick() {

    }
}

Quest.propTypes = {
    quest: React.PropTypes.object.isRequired
};


class Quests extends React.Component {

    render() {
        var quests = this.props.quests;

        if (quests !== null) {
            var items = _.map(quests, (quest) => {
                return (
                    <Quest key={quest.id}
                        quest={quest}
                        />
                );
            });

            return (
                <div className="card">
                    <div className="listview lv-bordered lv-lg quests">
                        <div className="lv-header-alt clearfix">
                            <h2 className="lvh-label hidden-xs">Availale quests</h2>
                        </div>
                        <div className="lv-body">
                            {items}
                        </div>
                    </div>
                </div>
            );
        } else {
            return <div className="card">Loading...</div>;
        }
    }
}

Quests.propTypes = {
    quests: React.PropTypes.object
};


export default class FluxQuests extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                questsStore: store => ({
                    quests: store.getQuests()
                }),
            }}>
                <Quests {...this.props}/>
            </FluxComponent>
        );
    }
}
