import axios from "axios";

export const signUp = async (credentials) => {
    try {
        const response = await axios.post(
            "/api/users",
            JSON.stringify(credentials),
            {
                headers: {
                    "Content-Type": "application/json"
                }
            });
        return response.data;
    } catch (error) {
        throw error;
    }
};