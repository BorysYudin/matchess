import {combineReducers} from "redux";
import {connectRouter} from 'connected-react-router'
import auth from "./auth.reducer";


const createRootReducer = history => combineReducers({
    router: connectRouter(history),
    auth
});

export default createRootReducer;
