import React from 'react';
import {connect} from 'react-redux';
import PropTypes from "prop-types";

import SignupForm from '../forms/SignupForm';
import {authSelectors} from "../../_selectors";


function SignupDialog(props) {
    return (
        <div>
            {props.errors && <p>{JSON.stringify(props.errors, null, 2)}</p>}
            <button onClick={props.handleClose}>Close</button>
            <SignupForm handleSignup={props.handleSignup}/>
        </div>
    )
}

function mapStateToProps(state) {
    return {
        errors: authSelectors.getSignupErrors(state)
    };
}

export default connect(mapStateToProps)(SignupDialog);

SignupDialog.propTypes = {
    handleSignup: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired,
    errors: PropTypes.object
};
