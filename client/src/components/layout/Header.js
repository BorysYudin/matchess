import React from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';

import {LOGIN_FORM, SIGNUP_FORM} from "../../_helpers/constants";
import LoginDialog from '../../components/dialogs/LoginDialog';
import SignupDialog from '../../components/dialogs/SignupDialog';
import {authActions} from '../../_actions';
import {authSelectors} from '../../_selectors';


class Header extends React.Component {
    state = {
        dialog: null
    };

    constructor(props) {
        super(props);

        this.closeDialog = this.closeDialog.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
    }

    displayDialog(form) {
        const dialogs = {
            LOGIN_FORM: <LoginDialog handleClose={this.closeDialog}
                                     handleLogin={this.handleLogin}/>,
            SIGNUP_FORM: <SignupDialog handleClose={this.closeDialog}
                                       handleSignup={this.handleSignup}/>
        };
        this.setState({dialog: dialogs[form]});
    }

    closeDialog() {
        this.setState({dialog: null});
    }

    handleSignup(data) {
        console.log('Signup:' + data);
    }

    handleLogin(e, data) {
        e.preventDefault();

        const {handleLogin} = this.props;
        handleLogin(data).then(this.closeDialog).catch(err => {});
    }

    render() {
        const {dialog} = this.state;
        const {isLoggedIn, handleLogout} = this.props;

        const logged_out_nav = (
            <ul>
                <li onClick={() => this.displayDialog(LOGIN_FORM)}>login</li>
                <li onClick={() => this.displayDialog(SIGNUP_FORM)}>signup</li>
            </ul>
        );

        const logged_in_nav = (
            <ul>
                <li onClick={handleLogout}>logout</li>
            </ul>
        );

        return (
            <header>
                {isLoggedIn ? logged_in_nav : logged_out_nav}
                {dialog}
            </header>
        );
    }
}

function mapStateToProps(state) {
    return {
        isLoggedIn: authSelectors.isLoggedIn(state)
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleLogout: () => dispatch(authActions.logout()),
        handleLogin: data => dispatch(authActions.login(data))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Header);

Header.propTypes = {
    isLoggedIn: PropTypes.bool.isRequired,
    handleLogout: PropTypes.func.isRequired,
    handleLogin: PropTypes.func.isRequired,
};

