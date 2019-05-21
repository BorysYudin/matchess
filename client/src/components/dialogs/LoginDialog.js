import React from 'react';
import PropTypes from "prop-types";

import LoginForm from '../forms/LoginForm';


function LoginDialog(props) {
    return (
        <div>
            <button onClick={props.handleClose}>Close</button>
            <LoginForm handleLogin={props.handleLogin}/>
        </div>
    )
}

export default LoginDialog;

LoginDialog.propTypes = {
    handleLogin: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired
};
