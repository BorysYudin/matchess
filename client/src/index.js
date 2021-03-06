import React from 'react';
import ReactDOM from 'react-dom';

import {Provider} from 'react-redux';
import {ConnectedRouter} from 'connected-react-router';
import {PersistGate} from 'redux-persist/lib/integration/react';

import {history, store, persistor} from './_helpers';
import App from './App';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(
    <Provider store={store}>
        <PersistGate persistor={persistor}>
            <ConnectedRouter history={history}>
                <App/>
            </ConnectedRouter>
        </PersistGate>
    </Provider>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
