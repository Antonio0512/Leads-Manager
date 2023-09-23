import {useEffect, useState} from "react";
import {createLead, getOneLead, updateLead} from "../services/leadService";

export const LeadModal = ({active, handleCancel, id, access_token, setError}) => {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        company: "",
        email: "",
        note: "",
    });

    useEffect(() => {
        const getLead = async () => {
            try {
                const result = await getOneLead(id, access_token);
                setFormData({
                    ...formData,
                    first_name: result.first_name,
                    last_name: result.last_name,
                    company: result.company,
                    email: result.email,
                    note: result.note,
                });
            } catch (error) {
                setError("Could not get lead");
            }
        };
        if (id) {
            getLead();
        } else {
            cleanFormData();
        }
    }, [id, access_token, setError]);

    const cleanFormData = () => {
        setFormData({
            first_name: "",
            last_name: "",
            company: "",
            email: "",
            note: "",
        });
    };

    const onChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

    const onUpdate = async (e) => {
        e.preventDefault();

        try {
            await updateLead(id, formData, access_token);
            cleanFormData();
            handleCancel();
        } catch (error) {
            setError(error.response.data.detail);
            handleCancel();
        }
    };

    const onCreate = async (e) => {
        e.preventDefault();

        try {
            await createLead(formData, access_token);
            cleanFormData();
            handleCancel();
        } catch (error) {
            setError(error.response.data.detail);
            handleCancel();
        }
    };

    return (
        <div className={`modal ${active && "is-active"}`}>
            <div className="modal-background" onClick={handleCancel}></div>
            <div className="modal-card">
                <header className="modal-card-head has-background-primary-light">
                    <h1 className="modal-card-title">{id ? "Update Lead" : "Create Lead"}</h1>
                </header>
                <section className="modal-card-body">
                    <form>
                        <div className="field">
                            <label className="label" htmlFor="first_name">First Name</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter first name"
                                       id="first_name"
                                       name="first_name"
                                       value={formData.first_name}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="given-name"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="last_name">Last Name</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter last name"
                                       id="last_name"
                                       name="last_name"
                                       value={formData.last_name}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="family-name"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="company">Company</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter company"
                                       id="company"
                                       name="company"
                                       value={formData.company}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="organization"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="email">Email</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter email"
                                       id="email"
                                       name="email"
                                       value={formData.email}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="email"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="note">Note</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter note"
                                       id="note"
                                       name="note"
                                       value={formData.note}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       autoComplete="off"
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    {id ? (
                        <button className="button is-info" onClick={(e) => onUpdate(e)}>
                            Update
                        </button>
                    ) : (
                        <button className="button is-primary" onClick={(e) => onCreate(e)}>
                            Create
                        </button>
                    )}
                    <button className="button" onClick={handleCancel}>
                        Cancel
                    </button>
                </footer>
            </div>
        </div>
    );
};
