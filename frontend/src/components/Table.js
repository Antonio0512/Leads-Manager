import {useContext, useEffect, useState} from "react";

import {LeadModal} from "./LeadModal";

import {deleteLead} from "../services/leadService";

import {UserContext} from "../context/UserContext";
import {LeadContext} from "../context/LeadContext";

import {ErrorMessage} from "./ErrorMessages";
import moment from "moment";

export const Table = () => {
    const {user} = useContext(UserContext);
    const {leads, getAllLeads} = useContext(LeadContext);
    const [error, setError] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);
    const [id, setId] = useState(null);

    useEffect(() => {
            const getLeads = async () => {
                try {
                    await getAllLeads();
                    setLoaded(true)
                } catch (error) {
                    setError(error);
                }
            }
            getLeads();
        }, []
    )

    const onUpdate = (lead_id) => {
        setId(lead_id);
        setActiveModal(true);
    };

    const onDelete = async (lead_id) => {
        try {
            await deleteLead(lead_id, user.access_token);
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    const onCreate = () => {
        setActiveModal(true);
    };

    const handleCancel = () => {
        setActiveModal(false);
        setId(null);
        getAllLeads();
    };

    return (
        <>
            <LeadModal
                active={activeModal}
                handleCancel={handleCancel}
                id={id}
                access_token={user.access_token}
                setError={setError}
            />
            <button className="button is-fullwidth mb-5 is-primary"
                    onClick={() => onCreate()}
            >
                Create Lead
            </button>
            <ErrorMessage message={error}/>
            {loaded && leads ? (
                <table className="table is-fullwidth">
                    <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Company</th>
                        <th>Email</th>
                        <th>Note</th>
                        <th>Last Updated</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {leads.map((lead) => (
                        <tr key={lead.id}>
                            <td>{lead.first_name}</td>
                            <td>{lead.last_name}</td>
                            <td>{lead.company}</td>
                            <td>{lead.email}</td>
                            <td>{lead.note}</td>
                            <td>{moment(lead.date_last_updated).format("MMM Do YY")}</td>
                            <td>
                                <button className="button mr-2 is-info is-light"
                                        onClick={() => onUpdate(lead.id)}>Update
                                </button>
                                <button className="button mr-2 is-danger is-light"
                                        onClick={() => onDelete(lead.id)}>Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            ) : (
                <p>Loading</p>
            )}
        </>
    );
};