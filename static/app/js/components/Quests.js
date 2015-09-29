'use strict';
import _ from 'lodash';
import Flux from 'flummox';
import FluxComponent from 'flummox/component';
import React from 'react';

import ProgressChart from './ProgressChart';
import QuestModal from './QuestModal';
import toString from '../utils/toString';
import { showErrors } from '../utils/notify';


class Quest extends React.Component {

    render() {
        var quest = this.props.quest;
        var activeQuest = this.props.activeQuest;

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

        var selectButton;
        if (activeQuest) {
            selectButton = (
                <ProgressChart
                    progress={activeQuest.progress / quest.duration * 100}
                    value={activeQuest.progress}
                    />
            );
        } else {
            selectButton = (
                <button onClick={this.props.onQuestSelect}
                    className="btn bgm-green btn-float waves-effect waves-effect waves-circle waves-float">
                    <i className="zmdi zmdi-directions-run"/>
                </button>
            );
        }

        return (
            <div className="lv-item media quest">
                <div className="buttons pull-left">
                    {selectButton}
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
}

Quest.propTypes = {
    quest: React.PropTypes.object.isRequired,
    activeQuest: React.PropTypes.object,
    onQuestSelect: React.PropTypes.func.isRequired
};


class Quests extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            showQuestId: null
        };
    }

    render() {
        var quests = this.props.quests;
        var city = this.props.city;

        if (quests !== null && city) {
            var showQuestModal;
            if (this.state.showQuestId) {
                const showQuest = quests[this.state.showQuestId];
                showQuestModal = (
                    <QuestModal quest={showQuest}
                        onHide={this.hideQuest.bind(this)}
                        onQuestStart={this.startQuest.bind(this, showQuest.id)}
                        />
                );
            }

            var items = _.map(quests, (quest) => {
                var activeQuest = city.active_quests[quest.id];
                return (
                    <Quest key={quest.id}
                        quest={quest}
                        activeQuest={activeQuest}
                        onQuestSelect={this.showQuest.bind(this, quest.id)}
                        />
                );
            });

            return (
                <div className="card modal-container">
                    <div className="listview lv-bordered lv-lg quests">
                        <div className="lv-header-alt clearfix">
                            <h2 className="lvh-label hidden-xs">Availale quests</h2>
                        </div>
                        <div className="lv-body">
                            {items}
                        </div>
                    </div>
                    {showQuestModal}
                </div>
            );
        } else {
            return <div className="card">Loading...</div>;
        }
    }

    hideQuest() {
        this.setState({showQuestId: null});
    }

    showQuest(questId) {
        this.setState({
            showQuestId: questId
        });
    }

    startQuest(questId) {
        this.props.flux.getActions('cityActions').startQuest(questId).catch(showErrors);
        this.hideQuest();
    }
}

Quests.propTypes = {
    quests: React.PropTypes.object,
    city: React.PropTypes.object,
    flux: React.PropTypes.instanceOf(Flux).isRequired
};


export default class FluxQuests extends React.Component {

    render() {
        return (
            <FluxComponent connectToStores={{
                questsStore: store => ({
                    quests: store.getQuests()
                }),
                cityStore: store => ({
                    city: store.getCity()
                })
            }}>
                <Quests {...this.props}/>
            </FluxComponent>
        );
    }
}
