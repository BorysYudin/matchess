import {HTTP} from '../_helpers';

const getData = (error = false) => response =>
    error ? Promise.reject(response.data) : response.data;

const login = data =>
    HTTP.post("/login", data).then(getData()).catch(getData(true));

const signup = data =>
    HTTP.post("/signup", data).then(getData()).catch(getData(true));

const authService = {
    login,
    signup
};

export default authService;
