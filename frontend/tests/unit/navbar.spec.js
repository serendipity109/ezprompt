import { mount } from '@vue/test-utils'
import NavBar from '@/components/NavBar.vue'

describe('NavBar.vue', () => {
  it('updates style and opacity based on the page prop', async () => {
    const wrapper = mount(NavBar, {
      props: {
        page: 'home',
      },
    })

    // Check that the home link has the correct style and opacity
    let homeLink = wrapper.find('a[href="/home"]')
    expect(homeLink.attributes('style')).toContain('opacity: 1')
    expect(homeLink.find('div.absolute').attributes('style')).toContain('border-bottom: 2.5px solid #6366f1')

    // Update the page prop
    await wrapper.setProps({ page: 'generate' })

    // Check that the home link now has the updated style and opacity
    homeLink = wrapper.find('a[href="/home"]')
    expect(homeLink.attributes('style')).toContain('opacity: 0.5')
    expect(homeLink.find('div.absolute').attributes('style')).toContain('border-bottom: 2.5px solid transparent')

    // Check that the generate link now has the correct style and opacity
    const generateLink = wrapper.find('a[href="/generate"]')
    expect(generateLink.attributes('style')).toContain('opacity: 1')
    expect(generateLink.find('div.absolute').attributes('style')).toContain('border-bottom: 2.5px solid #6366f1')
  })
})
