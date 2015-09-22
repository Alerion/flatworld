import React from 'react';
import { Link } from 'react-router';

export default class Sidebar extends React.Component {

    render() {
        return (
            <aside id="sidebar">
                <div classNameName="sidebar-inner c-overflow">
                    <div className="profile-menu">
                        <a href="">
                            <div className="profile-pic">
                                <img src={CONFIG.USER_AVATAR} alt={CONFIG.USER_NAME}/>
                            </div>

                            <div className="profile-info">
                                {CONFIG.USER_NAME}

                                <i className="zmdi zmdi-arrow-drop-down"></i>
                            </div>
                        </a>

                        <ul className="main-menu">
                            <li>
                                <a href="profile-about.html"><i className="zmdi zmdi-account"></i> View Profile</a>
                            </li>
                            <li>
                                <a href=""><i className="zmdi zmdi-input-antenna"></i> Privacy Settings</a>
                            </li>
                            <li>
                                <a href=""><i className="zmdi zmdi-settings"></i> Settings</a>
                            </li>
                            <li>
                                <a href=""><i className="zmdi zmdi-time-restore"></i> Logout</a>
                            </li>
                        </ul>
                    </div>

                    <ul className="main-menu">
                        <li>
                            <Link to="world" params={{worldId: CONFIG.WORLD_ID}}>
                                <i className="zmdi zmdi-globe"/> Map
                            </Link>
                        </li>
                        <li>
                            <Link to="building" params={{worldId: CONFIG.WORLD_ID}}>
                                <i className="zmdi zmdi-city"/> Building
                            </Link>
                        </li>
                        <li>
                            <Link to="units" params={{worldId: CONFIG.WORLD_ID}}>
                                <i className="zmdi zmdi-shield-security"/> Units
                            </Link>
                        </li>
                        <li>
                            <Link to="quest-demo" params={{worldId: CONFIG.WORLD_ID}}>
                                <i className="zmdi zmdi-pin-drop"/> Quests Demo
                            </Link>
                        </li>
                    </ul>
                </div>
            </aside>
        )
    }
}
