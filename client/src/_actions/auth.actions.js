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

    function failure(payload) {
        return {type: authConstants.LOGIN_FAILURE, payload};
    }

    return dispatch => {
        dispatch(request());

        return authService.login(data)
            .then(data => dispatch(success(data)))
            .catch(response => {
                dispatch(failure({
                    'message': 'Invalid username/password combination'
                }));
                return Promise.reject(response);
            });
    };
}

const authActions = {
    logout,
    login
};

export default authActions;
