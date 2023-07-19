<template>
    <div>
        <nav-bar page="account" :closePanel="closePanel"/>
        <div
            class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
            <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">
                <div class="pt-8 sm:pt-10 pb-16 container mx-auto max-w-6xl px-5 mb-32 sm:mb-0" @click="set_init">
                    <div class="sm:flex sm:flex-col sm:align-center">
                        <h1 class="mt-4 text-5xl md:text-6xl font-logo font-bold text-zinc-200 text-center">Memberships</h1>
                        <p class="mt-4 text-base text-zinc-200 text-center max-w-2xl m-auto">Choose a plan that works for
                            you.
                        </p>
                        <div class="relative self-center mt-10 sm:mt-14 bg-zinc-900 rounded-lg p-[6px] flex shadow">
                            <div class="absolute -top-6 right-2 text-sm text-zinc-200">Save 20%</div>
                            <button type="button" @click="plan = 1"
                                :class="{'bg-zinc-700 text-white': plan == 1, 'text-zinc-400': plan != 1}"
                                class='rounded-md py-2.5 text-sm font-medium whitespace-nowrap focus:outline-none focus:z-10 sm:w-auto sm:px-7 relative w-1/2'>Monthly
                                plans</button>
                            <button type="button" @click="plan = 2"
                                :class="{'bg-zinc-700 text-white': plan == 2, 'text-zinc-400': plan != 2}"
                                class='rounded-md py-2.5 text-sm font-medium whitespace-nowrap focus:outline-none focus:z-10 sm:w-auto sm:px-7 relative w-1/2'>Yearly
                                plans</button>                        </div>
                        <div class="my-8 space-y-8 md:mt-14 md:space-y-0 md:grid md:grid-cols-3 md:gap-6">
                            <div class="w-full relative rounded-lg shadow-sm bg-zinc-900 border border-transparent">
                                <div class="flex flex-col h-full p-6">
                                    <h2 class="text-2xl leading-6 font-semibold text-white">Starter</h2>
                                    <div class="mt-5 text-zinc-300 space-y-1">
                                        <div>- 1,000 fast generations per month.</div>
                                        <div>- No slow generations.</div>
                                        <div>- 2 parallel fast generations.</div>
                                        <div>- Commercial license (solo).</div>
                                        <div>- Images are public.</div>
                                    </div>
                                    <span class="mt-auto pt-7">
                                        <span v-if="plan == 1" class="text-5xl font-medium white">$10</span>
                                        <span v-if="plan == 2" class="text-5xl font-medium white">$8</span>
                                        <span class="text-base font-medium text-zinc-100">/ month</span>
                                        <p v-if="plan == 2" class="mt-2 ml-1 text-zinc-200 text-sm">Billed annually at $96/year</p>
                                    </span><button @click="topup(1)"
                                        class="mt-6 w-full h-11 flex items-center justify-center text-sm rounded-lg drop-shadow text-md px-8 py-2 shadow cursor-pointer active:scale-95 hover:brightness-110 transition-all bg-gradient-to-t from-indigo-600 via-indigo-600 to-indigo-500 ">&nbsp;Get
                                        started&nbsp;</button>
                                </div>
                            </div>
                            <div class="w-full relative rounded-lg shadow-sm bg-zinc-900 border border-transparent">
                                <div
                                    class="absolute top-0 right-5 px-4 py-2 text-xs font-medium tracking-wider text-white transform -translate-y-1/2 bg-red-700 rounded-full">
                                    Most Popular</div>
                                <div class="flex flex-col h-full p-6">
                                    <h2 class="text-2xl leading-6 font-semibold text-white">Pro</h2>
                                    <div class="mt-5 text-zinc-300 space-y-1">
                                        <div>- 3,000 fast generations per month.</div>
                                        <div>- Unlimited slow generations.</div>
                                        <div>- 3 parallel fast generations.</div>
                                        <div>- Commercial license.</div>
                                        <div>- Images are public.</div>
                                    </div><span class="mt-auto pt-7">
                                        <span v-if="plan == 1" class="text-5xl font-medium white">$30</span>
                                        <span v-if="plan == 2" class="text-5xl font-medium white">$24</span><span
                                            class="text-base font-medium text-zinc-100">/ month</span>
                                        <p v-if="plan == 2" class="mt-2 ml-1 text-zinc-200 text-sm">Billed annually at $288/year</p>
                                    </span><button @click="topup(2)"
                                        class="mt-6 w-full h-11 flex items-center justify-center text-sm rounded-lg drop-shadow text-md px-8 py-2 shadow cursor-pointer active:scale-95 hover:brightness-110 transition-all bg-gradient-to-t from-indigo-600 via-indigo-600 to-indigo-500 ">&nbsp;Get
                                        started&nbsp;</button>
                                </div>
                            </div>
                            <div class="w-full relative rounded-lg shadow-sm bg-zinc-900 border border-transparent">
                                <div
                                    class="absolute top-0 right-5 px-4 py-2 text-xs font-medium tracking-wider text-white transform -translate-y-1/2 bg-gray-700 rounded-full">
                                    Best Value</div>
                                <div class="flex flex-col h-full p-6">
                                    <h2 class="text-2xl leading-6 font-semibold text-white">Max</h2>
                                    <div class="mt-5 text-zinc-300 space-y-1">
                                        <div>- 7,000 fast generations per month.</div>
                                        <div>- Unlimited slow generations.</div>
                                        <div>- 3 parallel fast generations.</div>
                                        <div>- Commercial license.</div>
                                        <div>- Keep images private.</div>
                                    </div><span class="mt-auto pt-7">
                                        <span v-if="plan == 1" class="text-5xl font-medium white">$60</span>
                                        <span v-if="plan == 2" class="text-5xl font-medium white">$48</span><span
                                            class="text-base font-medium text-zinc-100">/ month</span>
                                        <p v-if="plan == 2" class="mt-2 ml-1 text-zinc-200 text-sm">Billed annually at $576/year</p>
                                    </span><button @click="topup(3)"
                                        class="mt-6 w-full h-11 flex items-center justify-center text-sm rounded-lg drop-shadow text-md px-8 py-2 shadow cursor-pointer active:scale-95 hover:brightness-110 transition-all bg-gradient-to-t from-indigo-600 via-indigo-600 to-indigo-500 ">&nbsp;Get
                                        started&nbsp;</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-12">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10">
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="plan-limit"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>How
                                    does the plan limit work?</h4>
                                <div class="text-zinc-400">If you go over your limit we'll nicely ask you to upgrade. You
                                    can
                                    create up to 100 images per month for free.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="fast"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>What
                                    are fast generations?</h4>
                                <div class="text-zinc-400">Every plan gets a set number of fast generations where your
                                    images
                                    are created using our fastest servers. On the Pro and Max plan you get unlimited
                                    generations, but we'll switch you over to our slower servers once you've hit your limit.
                                </div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="more-fast"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Can
                                    I
                                    buy more fast generations?</h4>
                                <div class="text-zinc-400">Yes, you can buy fast generations for $0.01 per generation. These
                                    never expire, but you must have an active plan to use them. Perfect for months where you
                                    need to go beyond your plan's limit. Just click the "Buy extra" button on your plan
                                    above.
                                </div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="upgrade"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Can
                                    I
                                    upgrade or downgrade my plan?</h4>
                                <div class="text-zinc-400">You can change plans at any time by choosing a new plan above. If
                                    you
                                    upgrade you will be pro-rated (only pay the difference). If you downgrade you will have
                                    a
                                    discount applied to future months.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="cancel"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>How
                                    do
                                    I cancel my plan?</h4>
                                <div class="text-zinc-400">You can cancel your plan at any time and keep access until the
                                    end of
                                    your billing period. To manage your plan, click the Manage Plan button above.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="private"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Do
                                    you
                                    accept PayPal?</h4>
                                <div class="text-zinc-400">We don't currently accept PayPal. You'll see all available
                                    payment
                                    methods on the checkout page after choosing a plan.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="private"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Can
                                    I
                                    keep my images private?</h4>
                                <div class="text-zinc-400">Images created under the Starter and Pro plans will show up in
                                    our
                                    search engine. If you subscribe to the Max plan then all your images will be private
                                    unless
                                    you decide to share them.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="commercial"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Can
                                    I
                                    use images for commercial purposes?</h4>
                                <div class="text-zinc-400">You can use any image you find on Lexica for personal use. For
                                    commercial use of images created with Lexica you must have a paid plan, with some
                                    restrictions on team size. If you're a team of 2-5 people then you need the Pro plan.
                                    Teams
                                    of 5+ need the Max plan. Please see our <a class="underline" href="license">license
                                        page</a>
                                    for more details on allowed usage.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="receipt"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Can
                                    you give me a receipt or invoice for tax purposes?</h4>
                                <div class="text-zinc-400">Click the manage plan button above to access your receipts and
                                    invoices.</div>
                            </div>
                            <div class="prose prose-indigo">
                                <h4 class="mb-2"><span class="mr-3 hidden target:!inline-flex" id="questions"><span
                                            class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-indigo-400 opacity-75"></span><span
                                            class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span></span>Where
                                    can I ask more questions?</h4>
                                <div class="text-zinc-400">Please join our <a class="underline"
                                        href="https://discord.gg/bMHBjJ9wRh" rel="noopener noreferrer"
                                        target="_blank">Discord
                                        community</a>. We're usually online and happy to answer any questions. You can also
                                    contact us at support@lexica.art</div>
                            </div>
                        </div>
                </div>
            </div>
        </div>
    </div>
</div></template>

<script>
import axios from "axios";
import { defineComponent, ref } from 'vue'
import NavBar from '@/components/NavBar.vue';
import { GET_TOKEN } from "@/store/storeconstants";
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default defineComponent({
    components: {
        NavBar
    },
    setup() {
        const plan = ref(1);
        const store = useStore()
        const closePanel = ref(true);
        const topup = async (n) => {
            const token = store.getters[`auth/${GET_TOKEN}`]
            if (token) {
                const credits = n*100
                const response = await axios.put(`http://${process.env.VUE_APP_BACKEND_IP}/user/top-up?credits=${credits}`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                })
                if (response.data.code == 200) {
                    const remaining_credits = response.data.result.remaining_credits
                    ElMessage.info("Successfully top-up credits.");
                    ElMessage.info(`Remaining credits: ${remaining_credits}`)
                } else {
                    ElMessage.error(response.data.message);
                }
            } else {
                ElMessage.error("Please log in.");
            }
        }
        const set_init = async () => {
            closePanel.value = !closePanel.value;
        }
        return { plan, topup, closePanel, set_init }
    }
})
</script>
