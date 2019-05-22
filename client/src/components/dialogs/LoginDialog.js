import React from 'react';
import {connect} from 'react-redux';
import PropTypes from "prop-types";

import LoginForm from '../forms/LoginForm';
import {authSelectors} from "../../_selectors";


function LoginDialog(props) {
    return (
        <div>
            {props.error && <p>{props.error}</p>}
            <button onClick={props.handleClose}>Close</button>
            <LoginForm handleLogin={props.handleLogin}/>
        </div>
    )
}

function mapStateToProps(state) {
    return {
        error: authSelectors.getError(state)
    };
}

export default connect(mapStateToProps)(LoginDialog);

LoginDialog.propTypes = {
    handleLogin: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired,
    error: PropTypes.string.isRequired
};
