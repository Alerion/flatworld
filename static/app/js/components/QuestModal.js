'use strict';
import React from 'react';
import { Button, Modal } from 'react-bootstrap';


export default class QuestModal extends React.Component {

    render() {
        var quest = this.props.quest;

        return (
            <Modal.Dialog bsSize="large"
                {...this.props}>
                <Modal.Header closeButton
                    onHide={this.props.onHide}>
                    <Modal.Title>{quest.name}</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    {quest.description}
                </Modal.Body>

                <Modal.Footer>
                    <Button onClick={this.props.onHide}>Close</Button>
                    <Button onClick={this.props.onQuestStart}
                        className="bgm-green">
                        Start
                    </Button>
                </Modal.Footer>
            </Modal.Dialog>
        );
    }
}


QuestModal.propTypes = {
    quest: React.PropTypes.object.isRequired,
    onHide: React.PropTypes.func.isRequired,
    onQuestStart: React.PropTypes.func.isRequired
};
