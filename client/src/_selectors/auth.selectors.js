const getAccessToken = state => state.auth.accessToken;
const isLoggedIn = state => Boolean(getAccessToken(state));
const getLoginErrors = state => state.auth.loginErrors;
const getSignupErrors = state => state.auth.signupErrors;

const authSelectors = {
    getAccessToken,
    getLoginErrors,
    getSignupErrors,
    isLoggedIn
};

export default authSelectors;