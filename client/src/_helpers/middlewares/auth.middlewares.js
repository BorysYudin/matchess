import moment from "moment";
import jwtDecode from "jwt-decode";

import {authActions} from "../../_actions";

function jwt({dispatch, getState}) {
    return next => action => {
        if (typeof action === "function") {
            const {auth} = getState();
            if (auth && auth.access_token) {
                // decode jwt so that we know if and when it expires
                const accessTokenExpiration = jwtDecode(auth.access_token).exp;

                if (
                    !accessTokenExpiration ||
                    moment(accessTokenExpiration * 1000) < moment(Date.now())
                )
                    dispatch(authActions.logout('Session expired'));
            }
        }
        return next(action);
    };
}

const authMiddlewares = {jwt};

export default authMiddlewares;
