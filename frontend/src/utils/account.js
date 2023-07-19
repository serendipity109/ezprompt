import axios from 'axios'


export async function getCredits (token) {
    try {
        const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_IP}/user/credits`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        if (response.data.data && 'credits' in response.data.data) {
            return response.data.data.credits;
        } else {
            console.error('Invalid response structure:', response.data);
        }
    } catch (error) {
        console.error('Failed to get credits:', error);
    }
}
