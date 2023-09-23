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

export const singIn = async (credentials) => {
    try {
        const response = await axios.post(
            "/api/login",
            JSON.stringify(
                `grant_type=&username=${credentials.email}&password=${credentials.password}&scope=&client_id=&client_secret=`
            ),
            {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};