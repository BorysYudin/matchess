import {combineReducers} from "redux";
import {connectRouter} from 'connected-react-router'
import auth from "./auth.reducer";
import user from "./user.reducer";


const createRootReducer = history => combineReducers({
    router: connectRouter(history),
    auth,
    user
});

export default createRootReducer;
