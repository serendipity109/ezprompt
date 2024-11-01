import {
  IS_USER_AUTHENTICATED,
  GET_USERNAME,
  GET_EMAIL,
  GET_TOKEN,
} from "../storeconstants";

export default {
  [IS_USER_AUTHENTICATED](state) {
    return state.authenticated;
  },

  [GET_USERNAME](state) {
    return state.username;
  },

  [GET_EMAIL](state) {
    return state.email;
  },
  [GET_TOKEN](state) {
    return state.token;
  },
};
