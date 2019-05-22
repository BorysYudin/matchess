import axios from 'axios';
import moment from "moment";
import jwtDecode from "jwt-decode";

import settings from '../settings';
import {store} from './store';
import {getAuthHeaders} from "./helpers";
import {authActions} from '../_actions';


const createResponseErrorInterceptor = store => error => {
    if (error.status === 401)
        store.dispatch(authActions.logout('Session expired'));

    return Promise.reject(error.response);
};

const createRequestInterceptor = store => config => {
    const {auth} = store.getState();
    console.log(auth);
    if (auth && auth.access_token) {
        // decode jwt so that we know if and when it expires
        const accessTokenExpiration = jwtDecode(auth.access_token).exp;

        if (
            !accessTokenExpiration ||
            moment(accessTokenExpiration * 1000) < moment(Date.now())
        )
            store.dispatch(authActions.logout('Session expired'));
    }

    return config;
};

const HTTP = axios.create({
    baseURL: `${settings.BASE_URL}/api/${settings.API_VERSION}`,
    headers: {
        ...getAuthHeaders()
    }
});

HTTP.interceptors.response.use(undefined, createResponseErrorInterceptor(store));
HTTP.interceptors.request.use(undefined, createRequestInterceptor(store));


export default HTTP;
