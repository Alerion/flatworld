'use strict';
import { Store } from 'flummox';
import Immutable from 'seamless-immutable';


export default class QuestsStore extends Store {

    constructor({ actions }) {
        super();

        this.actions = actions;
        this.registerAsync(actions.getQuests, this.startLoading, this.updateQuests);
        this.register(actions.updateQuests, this.updateQuests);
        this.state = {};
        this._loadingInProgress = false;
    }

    startLoading() {
        this._loadingInProgress = true;
    }

    updateQuests(obj) {
        this.setState({
            quests: Immutable(obj)
        });
        this._loadingInProgress = false;
    }

    getQuests() {
        if (! this.state.quests && ! this._loadingInProgress) {
            this.actions.getQuests();
            return null;
        }

        return this.state.quests;
    }
}
