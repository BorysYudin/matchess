import {authConstants} from "../_helpers/constants";

const initialState = {
    accessToken: '',
    error: ''
};

function auth(state = initialState, action) {
    switch (action.type) {
        case authConstants.LOGOUT:
            return initialState;

        default:
            return state;
    }
}

export default auth;
