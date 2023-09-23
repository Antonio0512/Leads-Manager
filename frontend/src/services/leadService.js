import axios from "axios";

export const getAllLeads = async () => {
    try {
        const response = await axios.get(
            "api/leads",
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getOneLead = async (lead_id, token) => {
    try {
        const response = await axios.get(
            `api/leads/${lead_id}`,
            {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            }
        )
        return response.data;
    } catch (error) {
        throw error;
    }
};


export const createLead = async (credentials, token) => {
    try {
        const response = await axios.post(
            "api/leads",
            JSON.stringify(credentials),
            {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateLead = async (lead_id, leadData, token) => {
    try {
        const response = await axios.put(
            `/api/leads/${lead_id}/update`,
            JSON.stringify(leadData),
            {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteLead = async (lead_id, token) => {
    try {
        const response = await axios.delete(
            `api/leads/${lead_id}/delete`,
            {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            }
        );
        return response.data;
    } catch (error) {
        throw error
    }
};