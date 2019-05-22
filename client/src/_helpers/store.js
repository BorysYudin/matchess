import thunk from 'redux-thunk';
import storage from "redux-persist/es/storage";
import autoMergeLevel2 from 'redux-persist/lib/stateReconciler/autoMergeLevel2';

import {createStore, applyMiddleware, compose} from 'redux';
import {routerMiddleware} from 'connected-react-router';
import {persistStore, persistReducer} from 'redux-persist';
import { createFilter } from "redux-persist-transform-filter";

import createRootReducer from '../_reducers';
import {createBrowserHistory as createHistory} from 'history';

export const history = createHistory();

const initialState = {};
const enhancers = [];
const middleware = [
    thunk,
    routerMiddleware(history)
];

if (process.env.NODE_ENV === 'development') {
    const devToolsExtension = window.__REDUX_DEVTOOLS_EXTENSION__;

    if (typeof devToolsExtension === 'function') {
        enhancers.push(devToolsExtension());
    }
}

const composedEnhancers = compose(
    applyMiddleware(...middleware),
    ...enhancers
);

const persistedFilter = createFilter("auth", [
    "accessToken"
]);

const persistConfig = {
    key: 'matchess',
    whitelist: ["auth"],
    transforms: [persistedFilter],
    stateReconciler: autoMergeLevel2,
    storage,
};

const rootReducer = createRootReducer(history);

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = createStore(
    persistedReducer,
    initialState,
    composedEnhancers
);
export const persistor = persistStore(store);
