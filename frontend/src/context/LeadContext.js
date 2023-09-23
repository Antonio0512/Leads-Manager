import {createContext, useState} from "react";
import * as leadService from "../services/leadService"

export const LeadContext = createContext(undefined);

export const LeadProvider = ({children}) => {
    const [leads, setLeads] = useState(null);

    const getAllLeads = async () => {
        try {
            const leadData = await leadService.getAllLeads();
            setLeads(leadData);
        } catch (error) {
            throw error;
        }
    };


    const createLead = async (credentials, token) => {
        try {
            return await leadService.createLead(credentials, token);
        } catch (error) {
            throw error;
        }
    };


    const leadContextData = {
        leads,
        getAllLeads,
        createLead
    }


    return (
        <LeadContext.Provider value={leadContextData}>
            {children}
        </LeadContext.Provider>
    )
};