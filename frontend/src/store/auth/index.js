import mutations from './mutations';
import getters from './getters';

export default {
    namespaced: true,
    state() {
        return {
            authenticated: false,
            username: "",
            email: "",
            token: "",
        }
    },
    mutations,
    getters
}