import { shallowMount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

describe('NavBar.vue', () => {
  it('should navigate correctly when goToPage is called', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [], // provide your routes here
    })

    const wrapper = shallowMount(NavBar, {
      global: {
        plugins: [router],
      },
      props: {
        page: 'home',
      },
    })

    // Mock the router.push function
    jest.spyOn(router, 'push')

    // Call the goToPage method
    await wrapper.vm.goToPage('/generate')

    // Assert that router.push was called with the right parameter
    expect(router.push).toHaveBeenCalledWith('/generate')
  })

  it('should correctly get navigation style and opacity based on page', () => {
    const wrapper = shallowMount(NavBar, {
      propsData: {
        page: 'home',
      },
    })

    expect(wrapper.vm.getNavStyle('home')).toBe('solid #6366f1')
    expect(wrapper.vm.getNavStyle('generate')).toBe('solid transparent')

    expect(wrapper.vm.getNavOpa('home')).toBe('1')
    expect(wrapper.vm.getNavOpa('generate')).toBe('0.5')
  })

    it('getNavStyle and getNavOpa return correct values when generate link is clicked', async () => {
    const wrapper = shallowMount(NavBar, {
      propsData: {
        page: '/generate',
      },
    })

    const generateLink = wrapper.find('a[v-on:click="goToPage(\'/generate\')"]')
    await generateLink.trigger('click')

    expect(wrapper.vm.getNavStyle('generate')).toBe('solid #6366f1')
    expect(wrapper.vm.getNavOpa('generate')).toBe('1')
  })
})
