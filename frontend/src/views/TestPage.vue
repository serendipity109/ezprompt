<!-- <template>
    <div>
        <div
            class="w-64 bg-gray-800 fixed z-50 right-0 top-5 rounded-md shadow text-sm flex flex-col items-start overflow-hidden border border-gray-700">
            <div class="px-4 py-2 bg-gray-700 w-full flex items-center">
                <div class="rounded-full h-7 w-7 flex items-center justify-center bg-gray-800 mr-2 text-white">
                    <p>{{ username_first_letter }}</p>
                </div>
                <span class="font-medium truncate text-white">{{ email }}</span>
            </div>
            <a class="w-full px-4 py-2 hover:bg-gray-700 flex justify-center text-white" href="/account">Account</a>
            <button @click="handleSignout" class="w-full px-4 py-2 hover:bg-gray-700 text-white">Sign out</button>
        </div>
    </div>
</template>
  
<script>
import { defineComponent, computed } from 'vue'
import { GET_EMAIL, GET_USERNAME, SET_AUTHENTICATION, SET_USERNAME, SET_EMAIL } from "@/store/storeconstants";
import { useStore } from 'vuex'

export default defineComponent({
    setup() {
        const store = useStore()
        const email = computed(() => {
            let Email = store.getters[`auth/${GET_EMAIL}`]
            return Email;
        });
        const username = computed(() => {
            let userName = store.getters[`auth/${GET_USERNAME}`]
            return userName;
        });
        const username_first_letter = computed(() => {
            let userName = username.value;
            return (typeof userName === 'string' && userName.length > 0) ? userName[0] : '';
        });
        const handleSignout = () => {
            store.commit(`auth/${SET_AUTHENTICATION}`, false);
            store.commit(`auth/${SET_USERNAME}`, "");
            store.commit(`auth/${SET_EMAIL}`, "");
        };
        return {
            email,
            username,
            username_first_letter,
            handleSignout
        }
    }
})
</script>
   -->
