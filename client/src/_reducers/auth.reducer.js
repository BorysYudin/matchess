import {authConstants} from "../_helpers/constants";

const initialState = {
    accessToken: '',
    loginErrors: null,
    signupErrors: null,
};

function auth(state = initialState, action) {
    switch (action.type) {
        case authConstants.LOGIN_SUCCESS:
        case authConstants.SIGNUP_SUCCESS:
            return {...initialState, accessToken: action.payload.token};

        case authConstants.LOGIN_FAILURE:
            return {...initialState, loginErrors: action.payload.errors};

        case authConstants.SIGNUP_FAILURE:
            return {...initialState, signupErrors: action.payload.errors};

        case authConstants.LOGOUT:
            return initialState;

        default:
            return state;
    }
}

export default auth;
