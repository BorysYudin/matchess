import {authConstants} from "../_helpers/constants";

const initialState = {
    accessToken: '',
    error: ''
};

function auth(state = initialState, action) {
    switch (action.type) {
        case authConstants.LOGIN_SUCCESS:
            return {...initialState, accessToken: action.payload.token};
        case authConstants.LOGIN_FAILURE:
            return {...initialState, error: action.payload.message};
        case authConstants.LOGOUT:
            return initialState;

        default:
            return state;
    }
}

export default auth;
