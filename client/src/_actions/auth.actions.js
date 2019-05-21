import { authConstants } from '../_helpers/constants';

const logout = () => ({
   type: authConstants.LOGOUT
});

const authActions = {
    logout
};

export default authActions;
