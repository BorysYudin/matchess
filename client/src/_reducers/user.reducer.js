import {authConstants} from "../_helpers/constants";

const initialState = {
    username: '',
    errors: null
};

function user(state = initialState, action) {
    switch (action.type) {
        case authConstants.LOGIN_SUCCESS:
        case authConstants.SIGNUP_SUCCESS:
            return {...initialState, username: action.payload.username};

        case authConstants.LOGOUT:
            return initialState;

        default:
            return state;
    }
}

export default user;
