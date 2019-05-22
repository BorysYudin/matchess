import {store} from "./store";


export const getAuthHeaders = () => {
    const {auth} = store.getState();

    return auth && auth.access_token
        ? { Authorization: `Bearer ${auth.access_token}` }
        : {};
};
