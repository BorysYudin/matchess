const getAccessToken = state => state.auth.accessToken;
const isLoggedIn = state => Boolean(getAccessToken(state));
const getError = state => state.auth.error;

const authSelectors = {
    getAccessToken,
    getError,
    isLoggedIn
};

export default authSelectors;