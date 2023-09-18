
export async function styleSelect (radio, type) {
    if (radio.value === '1') {
        type.value = '漫畫';
    } else if (radio.value == '2') {
        type.value = '電影';
    } else if (radio.value == '3') {
        type.value = '水墨畫';
    } else if (radio.value == '4') {
        type.value = '油畫';
    } else if (radio.value == '5') {
        type.value = '水彩畫';
    } else if (radio.value == '6') {
        type.value = '鉛筆畫';
    } else if (radio.value == '7') {
        type.value = '寫實';
    } else {
        type.value = null;
    }
}

