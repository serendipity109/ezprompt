import mockAxios from 'jest-mock-axios';
import { shallowMount } from "@vue/test-utils";
import NavBar from "@/components/NavBar.vue";

describe("NavBar.vue", () => {
  let wrapper;

  beforeEach(() => {
    // 清除所有未解決的請求和重設所有的模擬
    mockAxios.reset();

    wrapper = shallowMount(NavBar, {
      propsData: {
        page: "home",
      },
      stubs: {
        'v-dialog': {
          template: '<div><slot name="activator"></slot><slot></slot></div>',
        },
        'v-btn': {
          template: '<button @click="$emit(\'click\')"><slot/></button>',
        },
      },
    });
  });

  it("應該顯示正確的導覽欄標籤", () => {
    expect(wrapper.find("#homepage").text()).toBe("Home");
    expect(wrapper.find("#histpage").text()).toBe("History");
    expect(wrapper.find("#showpage").text()).toBe("Showcase");
    expect(wrapper.find("#accpage").text()).toBe("Account");
  });

  it("當當前頁面為首頁時，首頁標籤的透明度應為1", () => {
    expect(wrapper.vm.getNavOpa("home")).toBe("1");
  });

  it("當當前頁面不為首頁時，首頁標籤的透明度應為0.5", async () => {
    await wrapper.setProps({ page: "generate" });
    expect(wrapper.vm.getNavOpa("home")).toBe("0.5");
  });

  // it('當點擊 Get started 按鈕時，應該顯示登入視窗', async () => {
  //   expect(wrapper.vm.dialog).toBe(false)
  //   const button = wrapper.find('button')
  //   await button.trigger('click')
  //   expect(wrapper.vm.dialog).toBe(true)
  // });
});
