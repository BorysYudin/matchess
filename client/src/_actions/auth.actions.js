import {authService} from "../_services";
import {authConstants} from '../_helpers/constants';

const logout = (error = '') => ({
    type: authConstants.LOGOUT,
    error
});

function login(data) {
    function request() {
        return {type: authConstants.LOGIN_REQUEST}
    }

    function success(payload) {
        return {type: authConstants.LOGIN_SUCCESS, payload};
    }

    function failure(errors) {
        return {type: authConstants.LOGIN_FAILURE, payload: {errors}};
    }

    return dispatch => {
        dispatch(request());

        return authService.login(data)
            .then(data => dispatch(success(data)))
            .catch(data => dispatch(failure(data)));
    };
}

function signup(data) {
    function request() {
        return {type: authConstants.SIGNUP_REQUEST};
    }

    function success(payload) {
        return {type: authConstants.SIGNUP_SUCCESS, payload};
    }

    function failure(errors) {
        return {type: authConstants.SIGNUP_FAILURE, payload: {errors}};
    }

    return dispatch => {
        dispatch(request());

        return authService.signup(data)
            .then(data => dispatch(success(data)))
            .catch(data => dispatch(failure(data)));
    };
}

const authActions = {
    logout,
    login,
    signup
};

export default authActions;
