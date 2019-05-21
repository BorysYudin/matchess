import thunk from 'redux-thunk';
import { createBrowserHistory as createHistory } from 'history';
import storage from 'redux-persist/lib/storage';

import {createStore, applyMiddleware, compose} from 'redux'
import {routerMiddleware} from 'connected-react-router'
import {persistStore, persistReducer} from 'redux-persist';

import createRootReducer from '../_reducers';
import {authMiddlewares} from './middlewares';

export const history = createHistory();

const initialState = {};
const enhancers = [];
const middleware = [
    thunk,
    authMiddlewares.jwt,
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

const persistConfig = {
    key: 'matchess',
    storage: storage,
    whitelist: ['auth']
};

const rootReducer = createRootReducer(history);

const pReducer = persistReducer(persistConfig, rootReducer);

export const store = createStore(
    pReducer,
    initialState,
    composedEnhancers
);
export const persistor = persistStore(store);
