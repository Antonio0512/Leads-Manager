import {useContext, useEffect, useState} from "react";
import {UserContext} from "../context/UserContext";
import {LeadContext} from "../context/LeadContext";
import {ErrorMessage} from "./ErrorMessages";
import moment from "moment";
import {LeadModal} from "./LeadModal";

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

    const handleModal = () => {
        setActiveModal(!activeModal);
        getAllLeads();
    };

    return (
        <>
            <LeadModal active={activeModal}
                       handleModal={handleModal}
                       id={id}
                       access_token={user.access_token}
                       setError={setError}
            />
            <button className="button is-fullwidth mb-5 is-primary"
                    onClick={() => setActiveModal(true)}
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
                                <button className="button mr-2 is-info is-light">Update</button>
                                <button className="button mr-2 is-danger is-light">Delete</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            ) : (<p>Loading</p>)}
        </>
    );
};