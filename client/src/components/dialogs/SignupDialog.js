import React from 'react';
import PropTypes from "prop-types";

import SignupForm from '../forms/SignupForm';


function SignupDialog(props) {
    return (
        <div>
            <button onClick={props.handleClose}>Close</button>
            <SignupForm handleSignup={props.handleSignup}/>
        </div>
    )
}

export default SignupDialog;

SignupDialog.propTypes = {
    handleSignup: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired
};
