import {HTTP} from '../_helpers';

const login = data => HTTP.post("/login", data).then(response => response.data);

const authService = {
    login
};

export default authService;
