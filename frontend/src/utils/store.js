import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';

export default createStore({
    state: {
        user: '',
        auth: false,
        email: '',
        token: ''
    },
    plugins: [
        createPersistedState({
            storage: window.sessionStorage
        })
    ],
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuth(state, auth) {
            state.auth = auth;
        },
        setEmail(state, email) {
            state.email = email;
        },
        setToken(state, token) {
            state.token = token;
        }
    }
});
