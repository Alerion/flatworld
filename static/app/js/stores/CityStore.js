'use strict';
import { Store } from 'flummox';
import Immutable from 'seamless-immutable';
import _ from 'lodash';


export default class CityStore extends Store {

    constructor({ actions }) {
        super();

        this.actions = actions;
        this.registerAsync(actions.getCity, this.startLoading, this.updateCity);
        this.register(actions.build, this.updateCity);
        this.register(actions.startQuest, this.updateCity);
        this.register(actions.updateCity, this.updateCity);
        this.state = {};
        this._loadingInProgress = false;

        setInterval(this._updateBuildProgress.bind(this), 1000);
        setInterval(this._updateQuestsProgress.bind(this), 1000);
    }

    startLoading() {
        this._loadingInProgress = true;
    }

    updateCity(obj) {
        this.setState({
            city: Immutable(obj)
        });
        this._loadingInProgress = false;
    }

    getCity() {
        if (! this.state.city && ! this._loadingInProgress) {
            this.actions.getCity();
            return null;
        }

        return this.state.city;
    }

    _updateBuildProgress() {
        if (! this.state.city) {
            return;
        }

        var updates = {};
        _.forIn(this.state.city.buildings, function(building, id) {
            if (building.in_progress && building.build_progress > 0) {
                updates[id] = {
                    build_progress: building.build_progress - 1
                };
            }
        });

        if (! _.isEmpty(updates)) {
            var buildings = this.state.city.buildings.merge(updates, {deep: true});
            // FIXME: Do not update whole city.
            this.setState({
                city: this.state.city.merge({buildings: buildings})
            });
        }
    }

    _updateQuestsProgress() {
        if (! this.state.city) {
            return;
        }

        var updates = {};
        _.forIn(this.state.city.active_quests, function(quest, id) {
            if (quest.progress && quest.progress > 0) {
                updates[id] = {
                    progress: quest.progress - 1
                };
            }
        });

        if (! _.isEmpty(updates)) {
            var active_quests = this.state.city.active_quests.merge(updates, {deep: true});
            // FIXME: Do not update whole city.
            this.setState({
                city: this.state.city.merge({active_quests: active_quests})
            });
        }
    }
}
